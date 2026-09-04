**Pull Request Simulation**
Target Repository: TryGhost/Ghost
Base Branch: main
Compare Branch: fix/members-stripe-webhook-state-reconciliation
Author: Support Operations Engineering

**PR Title**
fix(members): add idempotent state reconciliation for interrupted Stripe subscription webhooks

**Description
Summary of Change**
When a publisher's subscriber completes checkout or updates a billing plan, Ghost relies on incoming customer.subscription.updated webhooks from Stripe to update the internal members and members_stripe_customers_subscriptions database tables.
Under rare network timeouts (HTTP 504) or transient worker interruptions, the webhook event may fail to process immediately. This leaves the subscriber in an incomplete or free state in the Ghost database despite an active billing state in Stripe.

**This PR introduces an idempotent reconciliation fallback inside the Members Service layer:**
When a member requests tier-gated content and local database state indicates incomplete while possessing an active subscription_id, an asynchronous background verification queries the Stripe API.
If Stripe confirms status as active, the local record is updated atomically using a Knex transaction without blocking the active request thread.
Emits an internal telemetry event for observability in support monitoring.

**Code Diff (Simulated)**
// File: ghost/core/core/server/services/members/service.js

async function verifyAndReconcileSubscriptionState(memberId, subscriptionId) {
    const localSubscription = await knex('members_stripe_customers_subscriptions')
        .where({ member_id: memberId, subscription_id: subscriptionId })
        .first();

    if (localSubscription && localSubscription.status === 'incomplete') {
        try {
            const stripeSubscription = await stripe.subscriptions.retrieve(subscriptionId);
            
            if (stripeSubscription && stripeSubscription.status === 'active') {
                await knex.transaction(async (trx) => {
                    await trx('members_stripe_customers_subscriptions')
                        .where({ subscription_id: subscriptionId })
                        .update({
                            status: 'active',
                            plan_id: stripeSubscription.items.data[0].price.id,
                            updated_at: new Date()
                        });

                    await trx('members')
                        .where({ id: memberId })
                        .update({
                            status: 'paid',
                            updated_at: new Date()
                        });
                });

                logging.info(`[SupportOps] Reconciled subscription ${subscriptionId} for member ${memberId}`);
            }
        } catch (err) {
            logging.warn(`[SupportOps] Fallback reconciliation skipped for ${subscriptionId}: ${err.message}`);
        }
    }


**Testing & Verification**
**Unit test:** Verified that valid active local subscriptions bypass external API queries.
**Integration test:** Simulated dropped webhook payload; verified subscriber unlocks tier content on subsequent request.
**Regression test:** Confirmed canceled and past_due subscriptions maintain expected access restrictions.
}

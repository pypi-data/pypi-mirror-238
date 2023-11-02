import sys

from . import billing
from . import context


def override_replace(metric, usage_override, usage_min, usage_max, usage_step):
    if usage_override is None:
        usage_override = []
    usage_min = None if usage_min is None else int(usage_min)
    usage_max = None if usage_max is None else int(usage_max)
    usage_step = None if usage_step is None else int(usage_step)
    for idx, x in enumerate(usage_override):
        if x["metric"] == metric:
            usage_override.remove(x)
    if usage_min is not None or usage_max or usage_step is not None:
        rec = {"metric": metric}
        if usage_min is not None:
            rec["min_quantity"] = usage_min
        if usage_max is not None:
            rec["max_quantity"] = usage_max
        if usage_step is not None:
            rec["step_quantity"] = usage_step
        usage_override.append(rec)
    return usage_override


def set_subscription_info(ctx, **kwargs):
    """Update various parameters associated with the subscription.
    e.g. the usage-metrics of min/max/step size."""
    result = billing.list_subscriptions(ctx, org_id=kwargs["org_id"])

    for bi in result.billing_subscriptions:
        billing_account_id = bi.spec.billing_account_id
        for org in bi.status.orgs:
            if org.id == kwargs["org_id"]:
                subscription_id = bi.metadata.id
                break

    if subscription_id is None:
        print(f"ERROR: could not find account info for {kwargs['org_id']}")
        sys.exit(1)

    subscription = billing.get_billing_subscription(
        ctx, billing_subscription_id=subscription_id
    )
    subscription_id = subscription.metadata.id
    usage_override = subscription.spec.usage_override

    usage_override = override_replace(
        "active_users",
        usage_override,
        kwargs["min_user"],
        kwargs["max_user"],
        kwargs["step_user"],
    )
    usage_override = override_replace(
        "active_connectors",
        usage_override,
        kwargs["min_connector"],
        kwargs["max_connector"],
        kwargs["step_connector"],
    )

    subscription.spec.usage_override = usage_override

    billing.update_subscription(
        ctx, billing_subscription_id=subscription_id, subscription=subscription
    )
    res = billing.create_usage_record(ctx, billing_account_id=billing_account_id)
    print(res)


def _show_billing(ctx, org):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    billing_account = apiclient.billing_api.get_billing_account(
        billing_account_id=org.billing_account_id
    )
    if "billing_subscription_id" in org and org.billing_subscription_id is not None:
        subscription = apiclient.billing_api.get_subscription(
            billing_subscription_id=org.billing_subscription_id
        )

        cid = billing_account.spec.customer_id
        sid = subscription.spec.subscription_id
        surl = "https://dashboard.stripe.com"
        print(f" STRIPE ACCOUNT:   {cid:30} {surl}/customers/{cid}")
        print(f" STRIPE SUBSCRIPT: {sid:30} {surl}/subscriptions/{sid}")


def _show_usage(ctx, org_id):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    metrics = apiclient.org_api.get_usage_metrics(org_id=org_id).metrics
    print("USAGE\n METRIC                PEAK CURRENT")
    for metric in metrics:
        tname = metric.type
        if metric.type == "fileshare":
            tname = "share"
        print(
            f" {tname:20} {metric.provisioned.peak:5}   {metric.provisioned.current:5}"
        )


def _show_auth(ctx, org_id):
    """Sign-in usage."""
    dt_from = "-15d"
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    query_results = apiclient.audits_api.list_auth_records(
        dt_from=dt_from, org_id=org_id, event_name="Authentication Request", limit=500
    )
    pids = {}
    for r in query_results.auth_audits:
        if r.event == "Success" and r.result == "Success":
            pids[r.client_id] = pids.get(r.client_id, 0) + 1
    if len(pids):
        print("APPROXIMATE AUTHENTICATION")
        print(" CLIENT-ID                             AUTHS")
        for p in pids:
            print(f" {p:35}   {pids[p]:5}")
    else:
        print("NO AUTHENTICATION ACTIONS")


def _show_status(ctx, org_id, org, **kwargs):
    print("-----------------------------")
    if org is None:
        token = context.get_token(ctx)
        apiclient = context.get_apiclient(ctx, token)
        org = apiclient.org_api.get_org(org_id=org_id)
    print(f"NAME:    {org.organisation}")
    print(f"ID:      {org.id}")
    print(f"CREATED: {org.created}")
    print(f"SHARD:   {org.shard}")
    print(f"ISSUER:  {org.issuer}")
    print(f"STATUS:  {org.admin_state}")
    print(f"CLUSTER: {org.cluster}")
    _show_billing(ctx, org)
    _show_usage(ctx, org_id=org.id)
    _show_auth(ctx, org_id=org.id)
    print("")


def status(ctx, **kwargs):
    """Show snapshot of this org, trial, billing, usage, status."""
    if kwargs["org_id"]:
        _show_status(ctx, org_id=kwargs["org_id"], org=None)
    if kwargs["email"]:
        token = context.get_token(ctx)
        apiclient = context.get_apiclient(ctx, token)
        params = {}
        params["limit"] = 500
        org = apiclient.org_api.list_orgs(**params)
        for org in org.orgs:
            if org.contact_email == kwargs["email"]:
                _show_status(ctx, org_id=org.id, org=org)

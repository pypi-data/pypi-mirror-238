import enum

import marshmallow


class StatusEnum(enum.Enum):
    Active = 'Active'
    Inactive = 'Inactive'
    SubOfferOnly = 'SubOfferOnly'


class ViewabilityEnum(enum.Enum):
    ApplyToRun = 'ApplyToRun'
    Testing = 'Testing'
    Private = 'Private'
    Public = 'Public'
    Archived = 'Archived'


class PixelBehaviorEnum(enum.Enum):
    dedupe = 'dedupe'
    replace = 'replace'
    incrementConvAndRev = 'incrementConvAndRev'
    incrementRevOnly = 'incrementRevOnly'


class TrafficTypesEnum(enum.Enum):
    Email = 'Email'
    Contextual = 'Contextual'
    Display = 'Display'
    Search = 'Search'
    Social = 'Social'
    Native = 'Native'
    MobileAds = 'MobileAds'


class CreateOfferSchema(marshmallow.Schema):
    friendlyName = marshmallow.fields.Str(required=True)
    category = marshmallow.fields.Int(required=True)
    description = marshmallow.fields.Str()
    domain = marshmallow.fields.Int(required=True)
    customFallbackUrl = marshmallow.fields.Str(required=True)
    filterFallbackUrl = marshmallow.fields.Str(required=True)
    filterFallbackProduct = marshmallow.fields.Int(required=True)
    dayparting = marshmallow.fields.Dict()
    filters = marshmallow.fields.Dict()
    destination = marshmallow.fields.Dict(required=True)
    status = marshmallow.fields.Enum(enum=StatusEnum, required=True)
    viewability = marshmallow.fields.Enum(enum=ViewabilityEnum, required=True)
    scrub = marshmallow.fields.Int()
    defaultAffiliateConvCap = marshmallow.fields.Int(allow_none=True)
    lifetimeAffiliateClickCap = marshmallow.fields.Int(allow_none=True)
    trafficTypes = marshmallow.fields.List(marshmallow.fields.Enum(enum=TrafficTypesEnum))
    pixelBehavior = marshmallow.fields.Enum(enum=PixelBehaviorEnum, dump_default=PixelBehaviorEnum.dedupe)
    allowQueryPassthrough = marshmallow.fields.Bool(dump_default=False)
    allowPageviewPixel = marshmallow.fields.Bool(dump_default=False)
    allowForcedClickConversion = marshmallow.fields.Bool(dump_default=False)
    unsubscribe_link = marshmallow.fields.Str()
    suppression_list = marshmallow.fields.Str()
    from_lines = marshmallow.fields.Str()
    subject_lines = marshmallow.fields.Str()
    redirectOffer = marshmallow.fields.Int(allow_none=True)
    redirectPercent = marshmallow.fields.Float(allow_none=True)
    capRedirectOffer = marshmallow.fields.Int(allow_none=True)


class AffiliateOfferSettingsSchema(marshmallow.Schema):
    affiliateId = marshmallow.fields.Integer(required=True)
    offerId = marshmallow.fields.Integer(required=True)
    status = marshmallow.fields.String(validate=lambda s: s in ['Applied', 'Denied', 'Approved'], required=True)
    trackingDomainOverride = marshmallow.fields.Integer(allow_none=True)
    conversionCapOverride = marshmallow.fields.Integer(allow_none=True)
    lifetimeClickCapOverride = marshmallow.fields.Integer(allow_none=True)
    queryPassthroughOverride = marshmallow.fields.Boolean(allow_none=True)
    offset = marshmallow.fields.Number(allow_none=True)
    pixel = marshmallow.fields.String(allow_none=True)
    pageview_pixel = marshmallow.fields.String(allow_none=True)
    pageview_postbacks = marshmallow.fields.Dict(
        keys=marshmallow.fields.Str(),
        values=marshmallow.fields.List(marshmallow.fields.String(), allow_none=True),
        allow_none=True
    )
    click_postbacks = marshmallow.fields.Dict(
        keys=marshmallow.fields.Str(),
        values=marshmallow.fields.List(marshmallow.fields.String(), allow_none=True),
        allow_none=True
    )
    simplePixels = marshmallow.fields.List(marshmallow.fields.Dict(
        pixelType=marshmallow.fields.String(validate=lambda s: s in ['FACEBOOK', 'TIKTOK']),
        eventName=marshmallow.fields.String(),
        eventSourceUrl=marshmallow.fields.String(),
        pixelId=marshmallow.fields.String(),
        accessToken=marshmallow.fields.String()
    ), allow_none=True)
    conversionEvents = marshmallow.fields.List(marshmallow.fields.Dict(
        id=marshmallow.fields.Integer(required=True),
        customerId=marshmallow.fields.String(required=True),
        conversionActionId=marshmallow.fields.String(required=True)
    ))
    postback = marshmallow.fields.List(marshmallow.fields.String())
    postbackMethods = marshmallow.fields.List(marshmallow.fields.String(validate=lambda s: s in ['GET', 'POST']))
    postbackBodies = marshmallow.fields.List(marshmallow.fields.String(allow_none=True))
    postbackHeaders = marshmallow.fields.List(marshmallow.fields.String(allow_none=True))
    redirectOffer = marshmallow.fields.Integer(allow_none=True)
    redirectPercent = marshmallow.fields.Float(validate=lambda f: 0 <= f <= 100, allow_none=True)
    capRedirectOffer = marshmallow.fields.Integer(allow_none=True)
    viewThrough = marshmallow.fields.List(marshmallow.fields.String())
    skipPostbackWhenRevLessThan = marshmallow.fields.Number(allow_none=True)
    mask_id = marshmallow.fields.String(allow_none=True)

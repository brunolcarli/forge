import graphene
from django.conf import settings
from api.models import Coin
from api.image_gen import generate_image
from api.solana_smith import deploy_coin


class CoinType(graphene.ObjectType):
    coin_name = graphene.String()
    coin_ticker = graphene.String()
    coin_image = graphene.String()
    signature = graphene.String()
    description = graphene.String()
    request_datetime = graphene.DateTime()

class Query:
    version = graphene.String()
    def resolve_version(self, info, **kwargs):
        return settings.VERSION

    coins = graphene.List(
        CoinType,
        name__icontains=graphene.String(),
        coin_ticker__icontains=graphene.String(),
        request_datetime=graphene.DateTime(),
        request_datetime__gte=graphene.DateTime(),
        request_datetime__lte=graphene.DateTime()
    )
    def resolve_coins(self, info, **kwargs):
        return Coin.objects.filter(**kwargs)


class CreateCoin(graphene.relay.ClientIDMutation):
    coin = graphene.Field(CoinType)

    class Input:
        name = graphene.String(required=True)
        ticker = graphene.String(required=True)
        image_prompt = graphene.String(required=True)
        description = graphene.String()

    def mutate_and_get_payload(self, info, **kwargs):
        img_path = generate_image(kwargs['image_prompt'])
        signature, img_blob = deploy_coin(kwargs['name'], kwargs['ticker'], img_path, description=kwargs.get('description'))

        coin = Coin.objects.create(coin_name=kwargs['name'], coin_ticker=kwargs['ticker'], coin_image=img_blob, signature=signature, description=kwargs.get('description'))
        coin.save()

        return CreateCoin(coin)


class Mutation:
    create_coin = CreateCoin.Field()

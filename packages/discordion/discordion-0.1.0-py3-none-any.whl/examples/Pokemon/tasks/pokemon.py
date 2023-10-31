from discordion.tasks import Task
from examples.Pokemon.models import Pokemon
from discordion.util import pick, enum_to_string


pokemons = [x.name for x in Pokemon.all()]


class CatchAPokemon(Task):
    description = f'Catch a Pokemon {{pokedex_number}} {{name}}, {{level}} (should be a number) which is type: {{type}} and caught in {{region_caught}}'

    async def run(self, args):
        pokemon = Pokemon.create(**pick(args, ['pokedex_number', 'name', 'level', 'type', 'region_caught']))
        await self.send_ai(f'Congratulations, you have caught {pokemon}')


class ListPokemons(Task):
    description = 'List all of the Pokemons you have caught {should_filter:0,1}'

    async def run(self, args):
        pokemons = "\n - ".join(str(x) for x in Pokemon.all())
        if int(args.get('should_filter', 0)):
            await self.send_ai(await self.embed(pokemons))
            return
        await self.send_ai(f'You have following Pokemons:\n - {pokemons}')


class FlushPokemons(Task):
    description = 'deletes all of the pokemons'

    async def run(self, args):
        Pokemon.flush()
        await self.send_ai(f'All pokemons released!')


class ReleaseOnePokemon(Task):
    description = f'Release a Pokemon {enum_to_string(pokemons, "name")} that you have caught'

    async def run(self, args):
        pokemon = Pokemon.where(name=args['name'])[0]
        pokemon.delete()
        await self.send_ai(f'Your {pokemon.name} has been released!')



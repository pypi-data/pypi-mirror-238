from discordion.tasks import Task
from examples.Pokemon.google import get_directions

from datetime import datetime


def journey_to_string(directions, a, b):
    def transit_string(step):
        return f'{step["vehicle"]}: line "{step["line"]}". You will get off at {step["destination"]}'

    def walking_string(step):
        return f'{step["destination"]} ({step["distance"]})'

    steps_string = '\n - '.join(walking_string(step) if step['vehicle'] == 'Walking' else transit_string(step) for step in directions[0]['steps'])
    return f'Next trip to {b} will be at {directions[0]["departure"]["text"]}. The duration is {directions[0]["duration"]["text"]} and you will be using following means of transportation: \n {steps_string}'


class CommuteHomeTask(Task):
    description = 'Gives commute directions and time of next departure from work to home'

    async def run(self, args):
        directions = get_directions('Novasol, virum', 'Stenhøj Have 23')
        await self.send_ai(journey_to_string(directions, 'Work', 'Home'))


class CommuteToWorkTask(Task):
    description = 'Gives commute directions and time of next departure from home to work'

    async def run(self, args):
        directions = get_directions('Stenhøj Have 23', 'Novasol, virum')
        await self.send_ai(journey_to_string(directions, 'Home', 'Work'))


class CommuteFromAtoBTask(Task):
    description = 'Gives you commuting directions from address/place {origin} to address/place {b}'

    async def run(self, args):
        directions = get_directions(args['origin'], args['b'])
        await self.send_ai(journey_to_string(directions, args['origin'], args['b']))


class CommuteFromHomeToB(Task):
    description = 'Gives you commuting directions from home to address/place {b}'

    async def run(self, args):
        directions = get_directions('Stenhøj Have 23', args['b'])
        await self.send_ai(journey_to_string(directions, 'Home', args['b']))


class CommuteFromAtoHomeTask(Task):
    description = 'Gives you commuting directions from address/place {a} to home'

    async def run(self, args):
        directions = get_directions(args['a'], 'Stenhøj Have 23')
        await self.send_ai(journey_to_string(directions, args['a'], 'Home'))


class CurrentDatetimeTask(Task):
    description = 'Response with the current time and date'

    async def run(self, args):
        await self.send_ai(f'currently it is: {datetime.now().strftime("%A, %d %B %Y %H:%M:%S")}')

from ..gpt import openai
import asyncio


async def predictBestTask(msg, tasks, retries=3):
    taskDefinitions = ';'.join(f'{task.__class__.__name__}: {task.description}' for task in tasks)
    taskMap = {task.__class__.__name__: task for task in tasks}
    messages = [
        {
            'role': 'system',
            'content': 'You are a classifier who based on a message will determine the best Task to process the request. First the user will give you a list of supported task and then they will give you a prompt that you have to map to the most appropriate task(s). format: Task1;var1:val1;var2:val2||Task2;var3:val3 etc.'
        },
        {
            'role': 'user',
            'content': taskDefinitions
        },
    ]

    history = []
    i = 0
    ref_msg = msg
    while ref_msg.reference:
        ref_msg = await ref_msg.channel.fetch_message(ref_msg.reference.message_id)

        print(ref_msg)

        history.append({
            'role': 'user' if i % 2 else 'assistant',
            'content': f'message: {ref_msg.content}' if i % 2 else ref_msg.content,
        })
        i += 1
    messages += history[::-1]
    messages.append(
        {
            'role': 'user',
            'content': f'message: {msg.content}'
        },
    )

    print(messages)

    try:
        response = openai.ChatCompletion.create(
            model='ft:gpt-3.5-turbo-0613:personal::8CuqaJhT',
            temperature=0,
            messages=messages
        )['choices'][0]['message']['content']
    except Exception as e:
        msg.channel.send('OpenAI\'s API is currently not available, try again later', reference=msg)
        print(e)
        return []

    print(response)
    response = response.strip(';').replace('<|im_sep|>', '').replace('=', ':')
    jobs = []
    for job in response.split('||'):
        print('job', job)
        args = dict()
        name = job
        if ';' in job:
            name, *argString = job.split(';')
            args = {x.split(':')[0].strip(' '): x.split(':')[1].strip(' ') for x in argString if ':' in x}
            print(name, args)
        jobs.append((type(taskMap[name])(), args))

    return jobs


async def improve_with_ai(msg, answer):
    history_string = '\n\n'.join(f'{msg["role"]}: {msg["content"]}' for msg in await history(msg))

    return openai.ChatCompletion.create(
        model='gpt-4',
        messages=[
            {
                'role': 'system',
                'content': 'You are a discord bot, you will receive a message + a proposed answer. your job is to make the proposed answer more natural whilst maintaining the meaning and all important information. Your message will be posted as a response on Discord, you will ensure the message is formatted to be displayed on Discord (feel free to use tables, emojis or any other discord styling that you deem suiting for the response). You responses will only contain the improved response.'
            },
            {
                'role': 'user',
                'content': f'HISTORY: {history_string} \n\n\nPROPOSED ANSWER: {answer}'
            },
        ]
    )['choices'][0]['message']['content']


async def history(msg):
    messages = [{
            'role': 'user',
            'content': msg.content
        }]
    is_user = True  # Start assuming that the first message is from the user

    while msg.reference:
        reference_message = await msg.channel.fetch_message(msg.reference.message_id)
        role = 'user' if is_user else 'assistant'
        content = f'message: {reference_message.content}' if is_user else reference_message.content

        messages.append({
            'role': role,
            'content': content
        })

        is_user = not is_user  # Toggle between user and assistant
        msg = reference_message  # Move to the referenced message for the next iteration

    return messages[::-1]


class TaskType(type):
    def __init__(cls, name, bases, attrs):
        if name != 'Task':
            Tasks.register(cls)
        super().__init__(name, bases, attrs)


class Tasks:
    tasks = []

    @classmethod
    def register(cls, task):
        cls.tasks.append(task())

    @classmethod
    async def run(cls, msg):
        output = []
        response = await msg.channel.send('Received your message :mailbox_with_mail:', reference=msg)
        tasks = await predictBestTask(msg, cls.tasks)
        i = 0
        for task, args in tasks:
            i += 1
            await response.edit(content=f'Thinking ({i}/{len(tasks)}) :thinking:')
            task.msg = msg
            await task.run(args)
            output.append(task.output)

        print(f'Executed all tasks, now to create an answer!')
        await response.edit(content=f'Done! Thinking of a way to politely answer :writing_hand:')

        print(output)
        # print('\n\n'.join('\n'.join(x) for x in output))
        output_string = '\n\n'.join('\n'.join(x) for x in output)
        message = await improve_with_ai(msg, output_string)
        print('improved response, now for updating discord')
        await response.edit(content=message)


class Task(metaclass=TaskType):
    def __init__(self):
        self.msg = None
        self.output = []

    async def run(self, args):
        return None

    async def send_ai(self, answer):
        self.output.append(answer)

    async def send(self, answer, **kwargs):
        self.msg.channel.send(answer, reference=self.msg, **kwargs)

    async def history(self):
        return history(self.msg)

    async def embed(self, data, question=None):
        question = question if question else self.msg.content

        messages = [
            {
                'role': 'system',
                'content': 'You are a helpful Discord bot assistant. Your job is to answer helpfully based on the information you are are granted'
            },
            {
                'role': 'assistant',
                'content': 'Hello there! In order to assist with your needs, can you give me some domain knowledge first?'
            },
            {
                'role': 'user',
                'content': f'Data: {data}. You are allowed to filter, sort, cherry-pick etc. on the data'
            },
            {
                'role': 'assistant',
                'content': 'Thank you very much! How may I assist you today?'
            },
            {
                'role': 'user',
                'content': question
            },
        ]

        return openai.ChatCompletion.create(
            model='gpt-4',
            messages=messages
        )['choices'][0]['message']['content']




class HelloTask(Task):
    description = 'greets a person'

    async def run(self, args):
        await self.send_ai('Howdy!')

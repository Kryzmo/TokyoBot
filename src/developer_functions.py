class dev():
    def __init__(self, client, cur, connection):
        self.client = client
        self.cur = cur
        self.connection = connection

    async def show_config(self, ctx):
        print(ctx)
        print('buraczki')

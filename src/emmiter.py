class emitter():
    def __init__(self):
      self.event_handlers = {}

    def on(self, event: str, handler):
      """Registra eventos"""
      if event not in self.event_handlers:
          self.event_handlers[event] = []
      self.event_handlers[event].append(handler)

    async def emit(self, event: str, *args):
        """Dispara eventos"""
        if event in self.event_handlers:
            for handler in self.event_handlers[event]:
                await handler(*args)
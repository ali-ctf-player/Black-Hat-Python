
from burp import IBurpExtender, IIntruderPayloadGeneratorFactory, IIntruderPayloadGenerator # type: ignore
from java.util import List, ArrayList # type: ignore
import random

class BurpExtender(IBurpExtender, IIntruderPayloadGeneratorFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName("BHP Payload Generator")
        callbacks.registerIntruderPayloadGeneratorFactory(self)
        return

    def getGeneratorName(self):
        return "BHP Payload Generator"

    def createNewInstance(self, attack):
        return BHPFuzzer(self,attack)
    


class BHPFuzzer(IIntruderPayloadGenerator):
    def __init__(self,extender,attack):
        self._extender = extender
        self._helpers = extender._helpers
        self._attack = attack
        self.max_payloads = 10
        self.num_iterations = 0
        return 

    def hasMorePayloads(self):
        return self.num_iterations < self.max_payloads

    def getNextPayload(self, current_payload):
        payload = "".join(chr(x) for x in current_payload)
        payload = self.mutatePayload(payload)

        self.num_iterations += 1
        return payload

    def reset(self):
        self.num_iterations = 0
        return

    def mutatePayload(self, original_payload):
        picker = random.randint(1,3)

        offset = random.randint(0,len(original_payload) - 1)
        payload = original_payload[:offset]

        # random offset insert a SQL injection attempt
        if picker == 1:
            payload += "'"

        # random offset insert a XSS attempt
        elif picker == 2:
            payload += "<script>alert('BHP!')</script>"
        
        else:
            chunk_length = random.randint(1,len(original_payload) - offset)
            repeater = random.randint(1,5)
            payload += original_payload[offset:offset+chunk_length] * repeater
            
        payload += original_payload[offset:]
        return payload


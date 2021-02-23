import automationhat
import time


class GeneralOutput:
    def __init__(self, *args, **kwargs):
        if automationhat.is_automation_hat():
            automationhat.light.power.write(1)

    # automationhat digital outputs
    def setbuzzerpin(self, time_):
        buzzer = automationhat.output.one
        buzzer.on()
        time.sleep(time_)
        buzzer.off()
        return None

    def resetbuzzerpin(self):
        buzzer = automationhat.relay.two
        buzzer.off()
        return None

    # automationhat onboard relays
    def setbarrierpin(self):
        bar = automationhat.relay.one
        bar.on()
        time.sleep(1)
        return None

    def resetbarrierpin(self):
        bar = automationhat.relay.one
        bar.off()
        return None


    def setlightpinred(self):
        light = automationhat.relay.two
        light.on()
        return None
        
    def setlightpingreen(self):
        light = automationhat.relay.two
        light.off()
        return None

import time

from bondzai.validation_framework.log_handler import logger
from bondzai.validation_framework.connector_handler import Connector
from bondzai.validation_framework.event_catcher import EventCatcher
from bondzai.gateway_sdk.enums import EventOperationID
from bondzai.gateway_sdk.agent import Agent, AgentTriggerType, AgentAIMode
from bondzai.gateway_sdk import Gateway
import sounddevice as sd
import keyboard
import sys


def training_is_done(agent: Agent, status):
    logger.info(f"EVT TRAIN : {status}")


def log_print(agent: Agent, log_message):
    logger.info(log_message)


def print_event(agent: Agent, event_id: EventOperationID, data: dict):
    logger.info(f"EVT {event_id.value} : {data}")


def print_event_final(agent: Agent, data: dict):
    logger.info(f"EVT FINALE {data}")


def print_event_infer(agent: Agent, data: dict):
    logger.info(f"EVT INFER {data}")


def set_callbacks(agent: Agent):
    # Set callbacks
    agent.on_log(log_print)
    agent.on_event(print_event)
    agent.on_training_done(training_is_done)
    agent.on_inference_done(print_event_infer)
    agent.on_final_process_result(print_event_final)


def force_train(agent: Agent):
    """
    Force agent to train
    """
    event_catcher = EventCatcher()
    agent.set_ai_mode(AgentAIMode.APP_AI_MODE_ENROLLEMENT, [0, 0])
    time.sleep(0.5)
    agent.set_ai_mode(AgentAIMode.APP_AI_MODE_INFERENCE)
    event_catcher.wait_training(agent)


class Keyboard_Listener:
    """
    Abstract keyboard listener object, for each OS, a child class must b defined
    """
    def __init__(self):
        """
        Initialise listener
        """
        self.agent_dict = {}
        self.hook = None
        self.to_stop = False

    def subscribe_agent(self, agent: Agent):
        if agent not in self.agent_dict.keys():
            self.agent_dict[agent] = False

    def start(self):

        def listen(keyEvent):
            result = None
            if keyEvent.event_type == keyboard.KEY_DOWN:
                result = self.on_press(keyEvent.name)
            elif keyEvent.event_type == keyboard.KEY_UP:
                result = self.on_release(keyEvent.name)
            return result

        self.hook = keyboard.hook(listen)
        while not self.to_stop:
            time.sleep(0.5)
        self.stop()

    def stop(self):
        keyboard.unhook(self.hook)

    def on_press(self, key: str):
        """
        Define event triggered when a key is pressed
        Args:
            key: pressed key
        """
        if key == "space":
            for agent, trigger in self.agent_dict.items():
                if not trigger:
                    agent.trigger(AgentTriggerType.TRIGGER_ON)
                    self.agent_dict[agent] = not trigger

    def on_release(self, key: str):
        """
        Define event triggered when a key is released
        Args:
            key: released key
        """
        if key == "q":
            self.to_stop = True
        if key == "space":
            for agent, trigger in self.agent_dict.items():
                if trigger:
                    agent.trigger(AgentTriggerType.TRIGGER_OFF)
                    self.agent_dict[agent] = not trigger


class AudioConnector(Connector):
    """
    Example of connector for audio stream (PC microphone)
    """
    def __init__(self):
        self.stream = None
        self.chunk_size = None
        super(AudioConnector, self).__init__()

    def open(self):
        """
        Open connection to sensor
        """
        default_device_idx = sd.default.device
        fs = 16000
        channel_nb = 1
        self.chunk_size = 1024

        try:
            self.stream = sd.InputStream(samplerate=fs, channels=channel_nb, device=default_device_idx,
                                         blocksize=self.chunk_size, dtype="int16")
            self.stream.start()
        except Exception:
            self.stream = None
            logger.error("Could not open stream, please check your device index / number of channels")
            sys.exit(1)

    def read(self, timeout: float = None):
        data = (self.stream.read(self.chunk_size)[0]).astype(float) / (2 ** 15)
        data = data.flatten().tolist()
        return data

    def close(self):
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()


def live_audio(agent: Agent):
    set_callbacks(agent)
    force_train(agent)
    keyboard_listen = Keyboard_Listener()
    keyboard_listen.subscribe_agent(agent)
    audioConnector = AudioConnector()
    audioConnector.subscribe_agent(agent, 1)
    audioConnector.open()
    audioConnector.start()
    audioConnector.start_sending()
    keyboard_listen.start()
    audioConnector.stop_sending()


if __name__ == "__main__":
    gateway = Gateway("127.0.0.1", 8765)
    gateway.connect()
    logger.info("WAITING ")
    agents = gateway.wait_for_agent()
    if agents:
        logger.info("STARTING ")
        current_agent = agents[0]
        current_agent.subscribe()
        live_audio(current_agent)

    gateway.close()


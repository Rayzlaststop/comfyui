import sys

import execution
import folder_paths
import impact.impact_server
from server import PromptServer
from impact.utils import any_typ
import impact.core as core


class ImpactCompare:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "cmp": (['a = b', 'a <> b', 'a > b', 'a < b', 'a >= b', 'a <= b', 'tt', 'ff'],),
                "a": (any_typ, ),
                "b": (any_typ, ),
            },
        }

    FUNCTION = "doit"
    CATEGORY = "ImpactPack/Logic"

    RETURN_TYPES = ("BOOLEAN", )

    def doit(self, cmp, a, b):
        if cmp == "a = b":
            return (a == b, )
        elif cmp == "a <> b":
            return (a != b, )
        elif cmp == "a > b":
            return (a > b, )
        elif cmp == "a < b":
            return (a < b, )
        elif cmp == "a >= b":
            return (a >= b, )
        elif cmp == "a <= b":
            return (a <= b, )
        elif cmp == 'tt':
            return (True, )
        else:
            return (False, )


class ImpactConditionalBranch:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "cond": ("BOOLEAN", {"forceInput": True}),
                "tt_value": (any_typ,),
                "ff_value": (any_typ,),
            },
        }

    FUNCTION = "doit"
    CATEGORY = "ImpactPack/Logic"

    RETURN_TYPES = (any_typ, )

    def doit(self, cond, tt_value, ff_value):
        if cond:
            return (tt_value,)
        else:
            return (ff_value,)


class ImpactConditionalStopIteration:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": { "cond": ("BOOLEAN", {"forceInput": True}), },
        }

    FUNCTION = "doit"
    CATEGORY = "ImpactPack/Logic"

    RETURN_TYPES = ()

    OUTPUT_NODE = True

    def doit(self, cond):
        if cond:
            PromptServer.instance.send_sync("stop-iteration", {})
        return {}


class ImpactNeg:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": { "value": ("BOOLEAN", {"forceInput": True}), },
        }

    FUNCTION = "doit"
    CATEGORY = "ImpactPack/Logic"

    RETURN_TYPES = ("BOOLEAN", )

    def doit(self, value):
        return (not value, )


class ImpactInt:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": ("INT", {"default": 0, "min": 0, "max": sys.maxsize, "step": 1}),
            },
        }

    FUNCTION = "doit"
    CATEGORY = "ImpactPack/Logic"

    RETURN_TYPES = ("INT", )

    def doit(self, value):
        return (value, )


class ImpactFloat:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": ("FLOAT", {"default": 1.0, "min": -3.402823466e+38, "max": 3.402823466e+38}),
            },
        }

    FUNCTION = "doit"
    CATEGORY = "ImpactPack/Logic"

    RETURN_TYPES = ("FLOAT", )

    def doit(self, value):
        return (value, )


class ImpactValueSender:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
                    "value": (any_typ, ),
                    "link_id": ("INT", {"default": 0, "min": 0, "max": sys.maxsize, "step": 1}),
                    },
                }

    OUTPUT_NODE = True

    FUNCTION = "doit"

    CATEGORY = "ImpactPack/Logic"

    RETURN_TYPES = ()

    def doit(self, value, link_id=0):
        PromptServer.instance.send_sync("value-send", {"link_id": link_id, "value": value})
        return {}


class ImpactIntConstSender:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
                    "signal": (any_typ, ),
                    "value": ("INT", {"default": 0, "min": 0, "max": sys.maxsize, "step": 1}),
                    "link_id": ("INT", {"default": 0, "min": 0, "max": sys.maxsize, "step": 1}),
                    },
                }

    OUTPUT_NODE = True

    FUNCTION = "doit"

    CATEGORY = "ImpactPack/Logic"

    RETURN_TYPES = ()

    def doit(self, signal, value, link_id=0):
        PromptServer.instance.send_sync("value-send", {"link_id": link_id, "value": value})
        return {}


class ImpactValueReceiver:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
                    "typ": (["STRING", "INT", "FLOAT", "BOOLEAN"], ),
                    "value": ("STRING", {"default": ""}),
                    "link_id": ("INT", {"default": 0, "min": 0, "max": sys.maxsize, "step": 1}),
                    },
                }

    FUNCTION = "doit"

    CATEGORY = "ImpactPack/Logic"

    RETURN_TYPES = (any_typ, )

    def doit(self, typ, value, link_id=0):
        if typ == "INT":
            return (int(value), )
        elif typ == "FLOAT":
            return (float(value), )
        elif typ == "BOOLEAN":
            return (bool(value), )
        else:
            return (value, )


class ImpactImageInfo:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
                    "value": ("IMAGE", ),
                    },
                }

    FUNCTION = "doit"

    CATEGORY = "ImpactPack/Logic/_for_test"

    RETURN_TYPES = ("INT", "INT", "INT", "INT")
    RETURN_NAMES = ("batch", "height", "width", "channel")

    def doit(self, value):
        return (value.shape[0], value.shape[1], value.shape[2], value.shape[3])


class ImpactMinMax:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
                    "mode": ("BOOLEAN", {"default": True, "label_on": "max", "label_off": "min"}),
                    "a": (any_typ,),
                    "b": (any_typ,),
                    },
                }

    FUNCTION = "doit"

    CATEGORY = "ImpactPack/Logic/_for_test"

    RETURN_TYPES = ("INT", )

    def doit(self, mode, a, b):
        if mode:
            return (max(a, b), )
        else:
            return (min(a, b),)


class ImpactQueueTrigger:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
                    "signal": (any_typ,),
                    "mode": ("BOOLEAN", {"default": True, "label_on": "Trigger", "label_off": "Don't trigger"}),
                    }
                }

    FUNCTION = "doit"

    CATEGORY = "ImpactPack/Logic/_for_test"
    RETURN_TYPES = (any_typ,)
    RETURN_NAMES = ("signal_opt",)
    OUTPUT_NODE = True

    def doit(self, signal, mode):
        if(mode):
            PromptServer.instance.send_sync("impact-add-queue", {})

        return (signal,)


class ImpactSetWidgetValue:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
                    "signal": (any_typ,),
                    "node_id": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                    "widget_name": ("STRING", {"multiline": False}),
                    },
                "optional": {
                    "boolean_value": ("BOOLEAN", {"forceInput": True}),
                    "int_value": ("INT", {"forceInput": True}),
                    "float_value": ("FLOAT", {"forceInput": True}),
                    "string_value": ("STRING", {"forceInput": True}),
                    }
                }

    FUNCTION = "doit"

    CATEGORY = "ImpactPack/Logic/_for_test"
    RETURN_TYPES = (any_typ,)
    RETURN_NAMES = ("signal_opt",)
    OUTPUT_NODE = True

    def doit(self, signal, node_id, widget_name, boolean_value=None, int_value=None, float_value=None, string_value=None, ):
        kind = None
        if boolean_value is not None:
            value = boolean_value
            kind = "BOOLEAN"
        elif int_value is not None:
            value = int_value
            kind = "INT"
        elif float_value is not None:
            value = float_value
            kind = "FLOAT"
        elif string_value is not None:
            value = string_value
            kind = "STRING"
        else:
            value = None

        if value is not None:
            PromptServer.instance.send_sync("impact-node-feedback",
                                            {"id": node_id, "widget_name": widget_name, "type": kind, "value": value})

        return (signal,)


class ImpactNodeSetMuteState:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
                    "signal": (any_typ,),
                    "node_id": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                    "set_state": ("BOOLEAN", {"default": True, "label_on": "active", "label_off": "mute"}),
                    }
                }

    FUNCTION = "doit"

    CATEGORY = "ImpactPack/Logic/_for_test"
    RETURN_TYPES = (any_typ,)
    RETURN_NAMES = ("signal_opt",)
    OUTPUT_NODE = True

    def doit(self, signal, node_id, set_state):
        PromptServer.instance.send_sync("impact-node-mute-state", {"id": node_id, "is_active": set_state})
        return (signal,)


error_skip_flag = False
try:
    import sys
    def filter_message(str):
        global error_skip_flag

        if "IMPACT-PACK-SIGNAL: STOP CONTROL BRIDGE" in str:
            return True
        elif error_skip_flag and "ERROR:root:!!! Exception during processing !!!\n" == str:
            error_skip_flag = False
            return True
        else:
            return False

    sys.__comfyui_manager_register_message_collapse(filter_message)

except Exception as e:
    print(f"e: {e}")
    pass


def workflow_to_map(workflow):
    nodes = {}
    links = {}
    for link in workflow['links']:
        links[link[0]] = link[1:]
    for node in workflow['nodes']:
        nodes[str(node['id'])] = node

    return nodes, links

class ImpactControlBridge:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
                      "value": (any_typ,),
                      "mode": ("BOOLEAN", {"default": True, "label_on": "pass", "label_off": "block"}),
                    },
                "hidden": {"unique_id": "UNIQUE_ID", "prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"}
                }

    FUNCTION = "doit"

    CATEGORY = "ImpactPack/Logic/_for_test"
    RETURN_TYPES = (any_typ,)
    RETURN_NAMES = ("value",)
    OUTPUT_NODE = True

    def doit(self, value, mode, unique_id, prompt, extra_pnginfo):
        global error_skip_flag

        nodes, links = workflow_to_map(extra_pnginfo['workflow'])

        outputs = [str(links[link][2]) for link in nodes[unique_id]['outputs'][0]['links']]

        prompt_set = set(prompt.keys())
        output_set = set(outputs)

        if mode:
            should_active_but_muted = output_set - prompt_set
            if len(should_active_but_muted) > 0:
                PromptServer.instance.send_sync("impact-bridge-continue", {"id": unique_id, 'actives': list(should_active_but_muted)})
                error_skip_flag = True
                raise Exception("IMPACT-PACK-SIGNAL: STOP CONTROL BRIDGE\nIf you see this message, your ComfyUI-Manager is outdated. Please update it.")
        else:
            should_muted_but_active = prompt_set.intersection(output_set)
            if len(should_muted_but_active) > 0:
                PromptServer.instance.send_sync("impact-bridge-continue", {"id": unique_id, 'mutes': list(should_muted_but_active)})
                error_skip_flag = True
                raise Exception("IMPACT-PACK-SIGNAL: STOP CONTROL BRIDGE\nIf you see this message, your ComfyUI-Manager is outdated. Please update it.")

        return (value, )


original_handle_execution = execution.PromptExecutor.handle_execution_error


def handle_execution_error(**kwargs):
    print(f" handled")
    execution.PromptExecutor.handle_execution_error(**kwargs)


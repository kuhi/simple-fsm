#testthisshit
from drawfsm import *

xml = """<fsm>
    <state label="name" id="1">
        <transition under="b">2</transition>
        <transition under="a">3</transition>
    </state>
    <state label="name2" id="2">
        <transition under="a">3</transition>
    </state>
    <state label="name3" id="3">
    </state>
</fsm>"""

fsm = parseXmlFromString(xml)
print(intoJavascript(fsm))
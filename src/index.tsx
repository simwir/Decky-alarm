import {
  ButtonItem,
  PanelSection,
  PanelSectionRow,
  Navigation,
  staticClasses
} from "@decky/ui";
import {
  addEventListener,
  removeEventListener,
  callable,
  definePlugin,
  toaster,
  // routerHook
} from "@decky/api"
import { useState } from "react";
import { FaClock, FaShip } from "react-icons/fa";

// import logo from "../assets/logo.png";

// This function calls the python function "add", which takes in two numbers and returns their sum (as a number)
// Note the type annotations:
//  the first one: [first: number, second: number] is for the arguments
//  the second one: number is for the return value
const add = callable<[first: number, second: number], number>("add");

// This function calls the python function "start_timer", which takes in no arguments and returns nothing.
// It starts a (python) timer which eventually emits the event 'timer_event'
const startTimer = callable<[], void>("start_timer");

const setAlarm = callable<[time: String, message: String], void>("set_alarm");
const setTimer = callable<[minutes: number, seconds: number, message: String], void>("set_timer");

function Content() {
  const [result, setResult] = useState<number | undefined>();

  const onClick = async () => {
    const result = await add(Math.random(), Math.random());
    setResult(result);
  };

  return (
    <PanelSection title="Panel Section">
      <PanelSectionRow>
        <ButtonItem
          layout="below"
          onClick={() => setAlarm("22:00", "22:00 alarm")}
        >
          {"Set alarm for 22:00"}
        </ButtonItem>
      </PanelSectionRow>
      <PanelSectionRow>
        <ButtonItem
          layout="below"
          onClick={() => setTimer(6, 0, "6 minute timer")}
        >
          {"Set 6 min timer"}
        </ButtonItem>
      </PanelSectionRow>      
      <PanelSectionRow>
        <ButtonItem
          layout="below"
          onClick={() => setTimer(0, 5, "5 second timer")}
        >
          {"Set 5 sec timer"}
        </ButtonItem>
      </PanelSectionRow>
      <PanelSectionRow>
        <ButtonItem
          layout="below"
          onClick={onClick}
        >
          {result ?? "Add two numbers via Python"}
        </ButtonItem>
      </PanelSectionRow>
      <PanelSectionRow>
        <ButtonItem
          layout="below"
          onClick={() => startTimer()}
        >
          {"Start Python timer"}
        </ButtonItem>
      </PanelSectionRow>

      {/* <PanelSectionRow>
        <div style={{ display: "flex", justifyContent: "center" }}>
          <img src={logo} />
        </div>
      </PanelSectionRow> */}

      {/*<PanelSectionRow>
        <ButtonItem
          layout="below"
          onClick={() => {
            Navigation.Navigate("/decky-plugin-test");
            Navigation.CloseSideMenus();
          }}
        >
          Router
        </ButtonItem>
      </PanelSectionRow>*/}
    </PanelSection>
  );
};

export default definePlugin(() => {
  console.log("Decky-alarm initializing")

  const notificationListener = addEventListener<[message: string]>(
    "notification_ringer", 
    (message) => {
      console.log("notificationRinger with message: ", message);
      toaster.toast({
        title: "Alarm",
        body: message
      });
    }
  )

  return {
    // The name shown in various decky menus
    name: "Decky alarm",
    // The element displayed at the top of your plugin's menu
    titleView: <div className={staticClasses.Title}>Decky alarm</div>,
    // The content of your plugin's menu
    content: <Content />,
    // The icon displayed in the plugin list
    icon: <FaClock />,
    // The function triggered when your plugin unloads
    onDismount() {
      console.log("Decky-alarm unloading")
      removeEventListener("notification_ringer", notificationListener);
      // serverApi.routerHook.removeRoute("/decky-plugin-test");
    },
  };
});

import { r as reactExports, u as useNavigate, j as jsxRuntimeExports, h as ResponsiveContainer, B as BarChart, C as CartesianGrid, X as XAxis, Y as YAxis, T as Tooltip, i as Bar } from "./vendors-67a83193.js";
import { a as activities } from "./activities-e215e445.js";
(function polyfill() {
  const relList = document.createElement("link").relList;
  if (relList && relList.supports && relList.supports("modulepreload")) {
    return;
  }
  for (const link of document.querySelectorAll('link[rel="modulepreload"]')) {
    processPreload(link);
  }
  new MutationObserver((mutations) => {
    for (const mutation of mutations) {
      if (mutation.type !== "childList") {
        continue;
      }
      for (const node of mutation.addedNodes) {
        if (node.tagName === "LINK" && node.rel === "modulepreload")
          processPreload(node);
      }
    }
  }).observe(document, { childList: true, subtree: true });
  function getFetchOpts(link) {
    const fetchOpts = {};
    if (link.integrity)
      fetchOpts.integrity = link.integrity;
    if (link.referrerPolicy)
      fetchOpts.referrerPolicy = link.referrerPolicy;
    if (link.crossOrigin === "use-credentials")
      fetchOpts.credentials = "include";
    else if (link.crossOrigin === "anonymous")
      fetchOpts.credentials = "omit";
    else
      fetchOpts.credentials = "same-origin";
    return fetchOpts;
  }
  function processPreload(link) {
    if (link.ep)
      return;
    link.ep = true;
    const fetchOpts = getFetchOpts(link);
    fetch(link.href, fetchOpts);
  }
})();
const MUNICIPALITY_CITIES_ARR = [
  "北京市",
  "上海市",
  "天津市",
  "重庆市",
  "香港特别行政区",
  "澳门特别行政区"
];
const LINE_OPACITY = 0.5;
const MAP_HEIGHT = 600;
const LIGHTS_ON = true;
const SHOW_ELEVATION_GAIN = false;
const IS_CHINESE = true;
const ZOOM_BIGMAP_LEVEL = 2;
const CHINESE_INFO_MESSAGE = (yearLength, year) => {
  const yearStr = year === "Total" ? "所有" : ` ${year} `;
  return `我用 App 记录自己运动 ${yearLength} 年了，下面列表展示的是${yearStr}的数据`;
};
const CHINESE_LOCATION_INFO_MESSAGE_FIRST = "勇敢地踏上旅程，你会发现，世界远比你想象的大。";
const CHINESE_LOCATION_INFO_MESSAGE_SECOND = "纵一苇之所如，凌万顷之茫然。";
const INFO_MESSAGE = CHINESE_INFO_MESSAGE;
const RUN_GENERIC_TITLE = "跑步";
const RUN_TRAIL_TITLE = "越野跑";
const RUN_TREADMILL_TITLE = "跑步机";
const HIKING_TITLE = "徒步";
const CYCLING_TITLE = "骑行";
const SKIING_TITLE = "滑雪";
const WALKING_TITLE = "步行";
const ACTIVITY_COUNT_TITLE = "活动次数";
const MAX_DISTANCE_TITLE = "最远距离";
const MAX_SPEED_TITLE = "最快速度";
const TOTAL_TIME_TITLE = "总时间";
const AVERAGE_SPEED_TITLE = "平均速度";
const TOTAL_DISTANCE_TITLE = "总距离";
const YEARLY_TITLE = "按年";
const MONTHLY_TITLE = "按月";
const WEEKLY_TITLE = "按周";
const DAILY_TITLE = "按天";
const LOCATION_TITLE = "位置";
const ACTIVITY_TYPES = {
  RUN_GENERIC_TITLE,
  RUN_TRAIL_TITLE,
  RUN_TREADMILL_TITLE,
  HIKING_TITLE,
  CYCLING_TITLE,
  SKIING_TITLE,
  WALKING_TITLE
};
const ACTIVITY_TOTAL = {
  ACTIVITY_COUNT_TITLE,
  MAX_DISTANCE_TITLE,
  MAX_SPEED_TITLE,
  TOTAL_TIME_TITLE,
  AVERAGE_SPEED_TITLE,
  TOTAL_DISTANCE_TITLE,
  YEARLY_TITLE,
  MONTHLY_TITLE,
  WEEKLY_TITLE,
  DAILY_TITLE,
  LOCATION_TITLE
};
const nike = "rgb(224,237,94)";
const dark_vanilla = "rgb(228,212,220)";
const NEED_FIX_MAP = false;
const MAIN_COLOR = nike;
const PROVINCE_FILL_COLOR = "#47b8e0";
const COUNTRY_FILL_COLOR = dark_vanilla;
const RUN_COLOR = MAIN_COLOR;
const RUN_TRAIL_COLOR = "rgb(255,153,51)";
const CYCLING_COLOR = "rgb(51,255,87)";
const HIKING_COLOR = "rgb(151,51,255)";
const WALKING_COLOR = HIKING_COLOR;
const SWIMMING_COLOR = "rgb(255,51,51)";
const activityList = "_activityList_1ukxg_1";
const filterContainer = "_filterContainer_1ukxg_7";
const summaryContainer = "_summaryContainer_1ukxg_23";
const activityCard = "_activityCard_1ukxg_30";
const activityName = "_activityName_1ukxg_45";
const activityDetails = "_activityDetails_1ukxg_51";
const chart = "_chart_1ukxg_60";
const smallHomeButton = "_smallHomeButton_1ukxg_70";
const styles = {
  activityList,
  filterContainer,
  summaryContainer,
  activityCard,
  activityName,
  activityDetails,
  chart,
  smallHomeButton
};
const ActivityCard = ({ period, summary, dailyDistances, interval, activityType }) => {
  const generateLabels = () => {
    if (interval === "month") {
      const [year, month] = period.split("-").map(Number);
      const daysInMonth = new Date(year, month, 0).getDate();
      return Array.from({ length: daysInMonth }, (_, i) => i + 1);
    } else if (interval === "week") {
      return Array.from({ length: 7 }, (_, i) => i + 1);
    } else if (interval === "year") {
      return Array.from({ length: 12 }, (_, i) => i + 1);
    }
    return [];
  };
  const data = generateLabels().map((day) => ({
    day,
    distance: (dailyDistances[day - 1] || 0).toFixed(2)
    // Keep two decimal places
  }));
  const formatTime = (seconds) => {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor(seconds % 3600 / 60);
    const s = Math.floor(seconds % 60);
    return `${h}h ${m}m ${s}s`;
  };
  const formatPace = (speed) => {
    if (speed === 0)
      return "0:00";
    const pace = 60 / speed;
    const minutes = Math.floor(pace);
    const seconds = Math.round((pace - minutes) * 60);
    return `${minutes}:${seconds < 10 ? "0" : ""}${seconds} min/km`;
  };
  const yAxisMax = Math.ceil(Math.max(...data.map((d) => parseFloat(d.distance))) + 10);
  const yAxisTicks = Array.from({ length: Math.ceil(yAxisMax / 5) + 1 }, (_, i) => i * 5);
  return /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: styles.activityCard, children: [
    /* @__PURE__ */ jsxRuntimeExports.jsx("h2", { className: styles.activityName, children: period }),
    /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: styles.activityDetails, children: [
      /* @__PURE__ */ jsxRuntimeExports.jsxs("p", { children: [
        /* @__PURE__ */ jsxRuntimeExports.jsxs("strong", { children: [
          ACTIVITY_TOTAL.TOTAL_DISTANCE_TITLE,
          ":"
        ] }),
        " ",
        summary.totalDistance.toFixed(2),
        " km"
      ] }),
      /* @__PURE__ */ jsxRuntimeExports.jsxs("p", { children: [
        /* @__PURE__ */ jsxRuntimeExports.jsxs("strong", { children: [
          ACTIVITY_TOTAL.AVERAGE_SPEED_TITLE,
          ":"
        ] }),
        " ",
        activityType === "ride" ? `${summary.averageSpeed.toFixed(2)} km/h` : formatPace(summary.averageSpeed)
      ] }),
      /* @__PURE__ */ jsxRuntimeExports.jsxs("p", { children: [
        /* @__PURE__ */ jsxRuntimeExports.jsxs("strong", { children: [
          ACTIVITY_TOTAL.TOTAL_TIME_TITLE,
          ":"
        ] }),
        " ",
        formatTime(summary.totalTime)
      ] }),
      interval !== "day" && /* @__PURE__ */ jsxRuntimeExports.jsxs(jsxRuntimeExports.Fragment, { children: [
        /* @__PURE__ */ jsxRuntimeExports.jsxs("p", { children: [
          /* @__PURE__ */ jsxRuntimeExports.jsxs("strong", { children: [
            ACTIVITY_TOTAL.ACTIVITY_COUNT_TITLE,
            ":"
          ] }),
          " ",
          summary.count
        ] }),
        /* @__PURE__ */ jsxRuntimeExports.jsxs("p", { children: [
          /* @__PURE__ */ jsxRuntimeExports.jsxs("strong", { children: [
            ACTIVITY_TOTAL.MAX_DISTANCE_TITLE,
            ":"
          ] }),
          " ",
          summary.maxDistance.toFixed(2),
          " km"
        ] }),
        /* @__PURE__ */ jsxRuntimeExports.jsxs("p", { children: [
          /* @__PURE__ */ jsxRuntimeExports.jsxs("strong", { children: [
            ACTIVITY_TOTAL.MAX_SPEED_TITLE,
            ":"
          ] }),
          " ",
          activityType === "ride" ? `${summary.maxSpeed.toFixed(2)} km/h` : formatPace(summary.maxSpeed)
        ] })
      ] }),
      interval === "day" && /* @__PURE__ */ jsxRuntimeExports.jsxs("p", { children: [
        /* @__PURE__ */ jsxRuntimeExports.jsxs("strong", { children: [
          ACTIVITY_TOTAL.LOCATION_TITLE,
          ":"
        ] }),
        " ",
        summary.location || ""
      ] }),
      ["month", "week", "year"].includes(interval) && /* @__PURE__ */ jsxRuntimeExports.jsx("div", { className: styles.chart, style: { height: "250px", width: "100%" }, children: /* @__PURE__ */ jsxRuntimeExports.jsx(ResponsiveContainer, { children: /* @__PURE__ */ jsxRuntimeExports.jsxs(BarChart, { data, margin: { top: 20, right: 20, left: -20, bottom: 5 }, children: [
        /* @__PURE__ */ jsxRuntimeExports.jsx(CartesianGrid, { strokeDasharray: "3 3", stroke: "#444" }),
        /* @__PURE__ */ jsxRuntimeExports.jsx(XAxis, { dataKey: "day", tick: { fill: "rgb(204, 204, 204)" } }),
        /* @__PURE__ */ jsxRuntimeExports.jsx(
          YAxis,
          {
            label: { value: "km", angle: -90, position: "insideLeft", fill: "rgb(204, 204, 204)" },
            domain: [0, yAxisMax],
            ticks: yAxisTicks,
            tick: { fill: "rgb(204, 204, 204)" }
          }
        ),
        /* @__PURE__ */ jsxRuntimeExports.jsx(
          Tooltip,
          {
            formatter: (value) => `${value} km`,
            contentStyle: { backgroundColor: "rgb(36, 36, 36)", border: "1px solid #444", color: "rgb(204, 204, 204)" },
            labelStyle: { color: "rgb(224, 237, 94)" }
          }
        ),
        /* @__PURE__ */ jsxRuntimeExports.jsx(Bar, { dataKey: "distance", fill: "rgb(224, 237, 94)" })
      ] }) }) })
    ] })
  ] });
};
const ActivityList = () => {
  const [interval, setInterval] = reactExports.useState("month");
  const [activityType, setActivityType] = reactExports.useState("run");
  const navigate = useNavigate();
  const toggleInterval = (newInterval) => {
    setInterval(newInterval);
  };
  const filterActivities = (activity) => {
    return activity.type.toLowerCase() === activityType;
  };
  const convertTimeToSeconds = (time) => {
    const [hours, minutes, seconds] = time.split(":").map(Number);
    return hours * 3600 + minutes * 60 + seconds;
  };
  const groupActivities = (interval2) => {
    return activities.filter(filterActivities).reduce((acc, activity) => {
      const date = new Date(activity.start_date_local);
      let key;
      let index;
      switch (interval2) {
        case "year":
          key = date.getFullYear().toString();
          index = date.getMonth();
          break;
        case "month":
          key = `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, "0")}`;
          index = date.getDate() - 1;
          break;
        case "week":
          const currentDate = new Date(date.valueOf());
          currentDate.setDate(currentDate.getDate() + 4 - (currentDate.getDay() || 7));
          const yearStart = new Date(currentDate.getFullYear(), 0, 1);
          const weekNum = Math.ceil(((currentDate.getTime() - yearStart.getTime()) / 864e5 + 1) / 7);
          key = `${currentDate.getFullYear()}-W${weekNum.toString().padStart(2, "0")}`;
          index = (date.getDay() + 6) % 7;
          break;
        case "day":
          key = date.toLocaleDateString("zh").replaceAll("/", "-");
          index = 0;
          break;
        default:
          key = date.getFullYear().toString();
          index = 0;
      }
      if (!acc[key])
        acc[key] = {
          totalDistance: 0,
          totalTime: 0,
          count: 0,
          dailyDistances: [],
          maxDistance: 0,
          maxSpeed: 0,
          location: ""
        };
      const distanceKm = activity.distance / 1e3;
      const timeInSeconds = convertTimeToSeconds(activity.moving_time);
      const speedKmh = timeInSeconds > 0 ? distanceKm / (timeInSeconds / 3600) : 0;
      acc[key].totalDistance += distanceKm;
      acc[key].totalTime += timeInSeconds;
      acc[key].count += 1;
      acc[key].dailyDistances[index] = (acc[key].dailyDistances[index] || 0) + distanceKm;
      if (distanceKm > acc[key].maxDistance)
        acc[key].maxDistance = distanceKm;
      if (speedKmh > acc[key].maxSpeed)
        acc[key].maxSpeed = speedKmh;
      if (interval2 === "day")
        acc[key].location = activity.location_country || "";
      return acc;
    }, {});
  };
  const activitiesByInterval = groupActivities(interval);
  return /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: styles.activityList, children: [
    /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: styles.filterContainer, children: [
      /* @__PURE__ */ jsxRuntimeExports.jsx(
        "button",
        {
          className: styles.smallHomeButton,
          onClick: () => navigate("/"),
          children: "Home"
        }
      ),
      /* @__PURE__ */ jsxRuntimeExports.jsxs("select", { onChange: (e) => setActivityType(e.target.value), value: activityType, children: [
        /* @__PURE__ */ jsxRuntimeExports.jsx("option", { value: "run", children: ACTIVITY_TYPES.RUN_GENERIC_TITLE }),
        /* @__PURE__ */ jsxRuntimeExports.jsx("option", { value: "ride", children: ACTIVITY_TYPES.CYCLING_TITLE })
      ] }),
      /* @__PURE__ */ jsxRuntimeExports.jsxs(
        "select",
        {
          onChange: (e) => toggleInterval(e.target.value),
          value: interval,
          children: [
            /* @__PURE__ */ jsxRuntimeExports.jsx("option", { value: "year", children: ACTIVITY_TOTAL.YEARLY_TITLE }),
            /* @__PURE__ */ jsxRuntimeExports.jsx("option", { value: "month", children: ACTIVITY_TOTAL.MONTHLY_TITLE }),
            /* @__PURE__ */ jsxRuntimeExports.jsx("option", { value: "week", children: ACTIVITY_TOTAL.WEEKLY_TITLE }),
            /* @__PURE__ */ jsxRuntimeExports.jsx("option", { value: "day", children: ACTIVITY_TOTAL.DAILY_TITLE })
          ]
        }
      )
    ] }),
    /* @__PURE__ */ jsxRuntimeExports.jsx("div", { className: styles.summaryContainer, children: Object.entries(activitiesByInterval).sort(([a], [b]) => {
      if (interval === "day") {
        return new Date(b).getTime() - new Date(a).getTime();
      } else if (interval === "week") {
        const [yearA, weekA] = a.split("-W").map(Number);
        const [yearB, weekB] = b.split("-W").map(Number);
        return yearB - yearA || weekB - weekA;
      } else {
        const [yearA, monthA = 0] = a.split("-").map(Number);
        const [yearB, monthB = 0] = b.split("-").map(Number);
        return yearB - yearA || monthB - monthA;
      }
    }).map(([period, summary]) => /* @__PURE__ */ jsxRuntimeExports.jsx(
      ActivityCard,
      {
        period,
        summary: {
          totalDistance: summary.totalDistance,
          averageSpeed: summary.totalTime ? summary.totalDistance / (summary.totalTime / 3600) : 0,
          totalTime: summary.totalTime,
          count: summary.count,
          maxDistance: summary.maxDistance,
          maxSpeed: summary.maxSpeed,
          location: summary.location
        },
        dailyDistances: summary.dailyDistances,
        interval,
        activityType
      },
      period
    )) })
  ] });
};
const HomePage = () => {
  return /* @__PURE__ */ jsxRuntimeExports.jsx("div", { children: /* @__PURE__ */ jsxRuntimeExports.jsx(ActivityList, {}) });
};
export {
  CYCLING_COLOR as C,
  HIKING_COLOR as H,
  IS_CHINESE as I,
  LIGHTS_ON as L,
  MAIN_COLOR as M,
  NEED_FIX_MAP as N,
  PROVINCE_FILL_COLOR as P,
  RUN_TRAIL_COLOR as R,
  SWIMMING_COLOR as S,
  WALKING_COLOR as W,
  ZOOM_BIGMAP_LEVEL as Z,
  MUNICIPALITY_CITIES_ARR as a,
  RUN_COLOR as b,
  SHOW_ELEVATION_GAIN as c,
  CHINESE_LOCATION_INFO_MESSAGE_FIRST as d,
  CHINESE_LOCATION_INFO_MESSAGE_SECOND as e,
  COUNTRY_FILL_COLOR as f,
  LINE_OPACITY as g,
  MAP_HEIGHT as h,
  INFO_MESSAGE as i,
  HomePage as j
};
//# sourceMappingURL=total-fb6203f0.js.map

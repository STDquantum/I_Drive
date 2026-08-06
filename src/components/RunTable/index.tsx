import React, { useState } from 'react';
import {
  sortDateFunc,
  sortDateFuncReverse,
  convertMovingTime2Sec,
  Activity,
  RunIds,
} from '@/utils/utils';
import { SHOW_ELEVATION_GAIN, SHOW_BPM } from "@/utils/const";

import RunRow from './RunRow';
import styles from './style.module.css';

interface IRunTableProperties {
  runs: Activity[];
  locateActivity: (_runIds: RunIds) => void;
  setActivity: (_runs: Activity[]) => void;
  month: string;
  onMonthChange: (_month: string) => void;
  runIndex: number;
  setRunIndex: (_index: number) => void;
}

type SortFunc = (_a: Activity, _b: Activity) => number;

const RunTable = ({
  runs,
  locateActivity,
  setActivity,
  month,
  onMonthChange,
  runIndex,
  setRunIndex,
}: IRunTableProperties) => {
  const [sortFuncInfo, setSortFuncInfo] = useState('');
  // TODO refactor?
  const sortKMFunc: SortFunc = (a, b) =>
    sortFuncInfo === 'KM' ? a.distance - b.distance : b.distance - a.distance;
  const sortElevationGainFunc: SortFunc = (a, b) =>
    sortFuncInfo === 'Elevation Gain'
      ? (a.elevation_gain ?? 0) - (b.elevation_gain ?? 0)
      : (b.elevation_gain ?? 0) - (a.elevation_gain ?? 0);
  const sortAvgVFunc: SortFunc = (a, b) =>
    sortFuncInfo === 'AvgKPH'
      ? b.average_speed - a.average_speed
      : a.average_speed - b.average_speed;
  const sortBPMFunc: SortFunc = (a, b) => {
    return sortFuncInfo === 'BPM'
      ? (a.average_heartrate ?? 0) - (b.average_heartrate ?? 0)
      : (b.average_heartrate ?? 0) - (a.average_heartrate ?? 0);
  };
  const sortRunTimeFunc: SortFunc = (a, b) => {
    const aTotalSeconds = convertMovingTime2Sec(a.moving_time);
    const bTotalSeconds = convertMovingTime2Sec(b.moving_time);
    return sortFuncInfo === 'Time'
      ? aTotalSeconds - bTotalSeconds
      : bTotalSeconds - aTotalSeconds;
  };
  const sortDateFuncClick =
    sortFuncInfo === 'Date' ? sortDateFunc : sortDateFuncReverse;
  const sortFuncMap = new Map([
    ['KM', sortKMFunc],
    ['Elevation Gain', sortElevationGainFunc],
    ['AvgKPH', sortAvgVFunc],
    ['BPM', sortBPMFunc],
    ['Time', sortRunTimeFunc],
    ['Date', sortDateFuncClick],
  ]);
  if (!SHOW_ELEVATION_GAIN){
    sortFuncMap.delete('Elevation Gain')
  }
  if (!SHOW_BPM) {
    sortFuncMap.delete('BPM');
  }

  const handleClick: React.MouseEventHandler<HTMLElement> = (e) => {
    const funcName = (e.target as HTMLElement).innerHTML;
    const f = sortFuncMap.get(funcName);

    setRunIndex(-1);
    setSortFuncInfo(sortFuncInfo === funcName ? '' : funcName);
    setActivity(runs.slice().sort(f));
  };

  return (
    <div className={styles.tableContainer}>
      <label className={styles.monthFilter}>
        <span>月份</span>
        <select value={month} onChange={(e) => onMonthChange(e.target.value)}>
          <option value="all">全部</option>
          {Array.from({ length: 12 }, (_, index) => {
            const monthValue = String(index + 1).padStart(2, '0');
            return (
              <option key={monthValue} value={monthValue}>
                {index + 1}月
              </option>
            );
          })}
        </select>
      </label>
      <div className={styles.tableScroll}>
        <table className={styles.runTable} cellSpacing="0" cellPadding="0">
          <thead>
            <tr>
              <th />
              {Array.from(sortFuncMap.keys()).map((k) => (
                <th key={k} onClick={handleClick}>
                  {k}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {runs.map((run, elementIndex) => (
              <RunRow
                key={run.run_id}
                elementIndex={elementIndex}
                locateActivity={locateActivity}
                run={run}
                runIndex={runIndex}
                setRunIndex={setRunIndex}
              />
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default RunTable;

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
  selectedRunIds: RunIds;
  onSelectionChange: (_runIds: RunIds) => void;
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
  selectedRunIds,
  onSelectionChange,
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

  const selectedRunIdSet = new Set(selectedRunIds);
  const selectedRuns = runs.filter((run) => selectedRunIdSet.has(run.run_id));
  const selectedDistance = selectedRuns.reduce(
    (total, run) => total + run.distance,
    0
  );
  const selectedElevation = selectedRuns.reduce(
    (total, run) => total + (run.elevation_gain ?? 0),
    0
  );
  const selectedTime = selectedRuns.reduce(
    (total, run) => total + convertMovingTime2Sec(run.moving_time),
    0
  );
  const selectedAverageSpeed = selectedTime
    ? (selectedDistance / 1000 / (selectedTime / 3600)).toFixed(1)
    : '0.0';
  const selectedTimeHours = (selectedTime / 3600).toFixed(1);

  const handleClick: React.MouseEventHandler<HTMLElement> = (e) => {
    const funcName = (e.target as HTMLElement).innerHTML;
    const f = sortFuncMap.get(funcName);

    setRunIndex(-1);
    setSortFuncInfo(sortFuncInfo === funcName ? '' : funcName);
    setActivity(runs.slice().sort(f));
  };

  const handleToggleSelection = (runId: number, isSelected: boolean) => {
    const nextSelectedRunIds = new Set(selectedRunIds);
    if (isSelected) {
      nextSelectedRunIds.add(runId);
    } else {
      nextSelectedRunIds.delete(runId);
    }
    onSelectionChange(Array.from(nextSelectedRunIds));
  };

  return (
    <div className={styles.tableContainer}>
      <div className={styles.selectionToolbar}>
        <span>已选择 {selectedRuns.length} 条路线</span>
        <button
          type="button"
          onClick={() => onSelectionChange(runs.map((run) => run.run_id))}
        >
          全选
        </button>
        <button type="button" onClick={() => onSelectionChange([])}>
          全部取消
        </button>
        {selectedRuns.length > 0 && (
          <>
            <span>{(selectedDistance / 1000).toFixed(2)} KM</span>
            {SHOW_ELEVATION_GAIN && (
              <span>{selectedElevation.toFixed(0)} Elevation Gain</span>
            )}
            <span>{selectedAverageSpeed} AvgKPH</span>
            <span>{selectedTimeHours} h</span>
          </>
        )}
      </div>
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
                selected={selectedRunIdSet.has(run.run_id)}
                onToggleSelection={handleToggleSelection}
              />
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default RunTable;

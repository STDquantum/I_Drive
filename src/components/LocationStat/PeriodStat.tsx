import Stat from '@/components/Stat';
import useActivities from '@/hooks/useActivities';

const PeriodStat = ({ onClick }: { onClick: (_period: string) => void }) => {
  const { runPeriod } = useActivities();

  const periodArr = Object.entries(runPeriod);
  periodArr.sort((a, b) => b[1] - a[1]);
  return (
    <div className="cursor-pointer">
      <section style={{
        maxHeight: '550px', // 设置最大高度为 550px
        overflowY: 'auto',  // 当内容超过最大高度时显示垂直滚动条
        border: '0px solid #ccc', // 为了便于观察，可以添加边框
        padding: '0px' // 添加一些内边距
      }}>
        {periodArr.map(([period, times]) => (
          <Stat
            key={period}
            value={period}
            description={` ${times} Runs`}
            citySize={3}
            onClick={() => onClick(period)}
          />
        ))}
      </section>
      <hr color="red" />
    </div>
  );
};

export default PeriodStat;

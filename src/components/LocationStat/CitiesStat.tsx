import Stat from '@/components/Stat';
import useActivities from '@/hooks/useActivities';

// only support China for now
const CitiesStat = ({ onClick }: { onClick: (_city: string) => void }) => {
  const { cities } = useActivities();

  const citiesArr = Object.entries(cities);
  citiesArr.sort((a, b) => b[1] - a[1]);
  return (
    <div className="cursor-pointer">
      <section style={{
        maxHeight: '350px', // 设置最大高度为 400px
        overflowY: 'auto',  // 当内容超过最大高度时显示垂直滚动条
        border: '0px solid #ccc', // 为了便于观察，可以添加边框
        padding: '0px' // 添加一些内边距
      }}>
        {citiesArr.map(([city, distance]) => (
          <Stat
            key={city}
            value={city}
            description={` ${(distance / 1000).toFixed(0)} KM`}
            citySize={3}
            onClick={() => onClick(city)}
          />
        ))}
      </section>
      <hr color="red" />
    </div>
  );
};

export default CitiesStat;

import MIG_1 from './mig_1.js';
import MIG_2 from './mig_2.js';

const MIG_1_StartRate = 1;
const MIG_2_StartRate = 1;


const timeUnit = '1s';

const preAllocatedVUs = 1;
const maxVUs = 2200;


const getStages = (startRate, increment, maxRps) => {
 let stages = [];
 let currentRps = startRate;
 while (currentRps <= maxRps) {
     stages.push({ duration: '1s', target: currentRps });
     stages.push({ duration: currentRps === maxRps ? '3600s' : '60s', target: currentRps });
     currentRps += increment; // увеличиваем RPS на 5 для следующего этапа
 }
 return stages;
}

const getOptions = (startRate, exec, maxRps) => {
    return{
        executor: 'ramping-arrival-rate',
        preAllocatedVUs,
        maxVUs,
        timeUnit,
        gracefulStop: '10s',
        startRate,
        stages: getStages(startRate, 100, maxRps),
        exec,
    }
}


export const options = {
    scenarios: {
        
       MIG_1: getOptions(MIG_1_StartRate, 'MIG_1_exec', 6000),

       MIG_2: getOptions(MIG_2_StartRate, 'MIG_2_exec', 6000),
    }
}


export function MIG_1_exec() {
   MIG_1();
}
export function MIG_2_exec() {
   MIG_2();
}
// C:\Program Files\k6\
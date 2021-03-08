import React, { useEffect, useState } from "react";
import { XYPlot, ChartLabel, VerticalGridLines, HorizontalGridLines, XAxis, YAxis, LineSeries } from 'react-vis';
import axios from "axios";
import '../node_modules/react-vis/dist/style.css';
import styles from "./stockclap.module.scss";
import Pacman from "react-spinners/PacmanLoader";

const Clicker=["open","close","high","low"]
export const StockClap = (props) => {
    const [chart, setChart] = useState([])
    const [loading, setLoading] = useState(false);
    const [idclicked,SetId]=useState(0)
    useEffect(() => {
        if (props.isin) {
            const chartfetcher = async () => {
                setLoading(true)
                const result = await axios.post('http://localhost:5000/api/chart', { isin: props.isin })
                    .then(res => res.data)
                setLoading(false)
                return result
            }
            chartfetcher()
                .then(res => setChart(res))
        }
    }, []);

    const handleClick =(id)=>{
        console.log(id)
        SetId(id)
    }
    return (
        <div className={styles.chart}>
            <div className={styles.innerbox} style={{marginTop: "2%"}}>
            <Pacman className={styles.innerbox} loading={loading} size={50} />
            </div>
            <div className={styles.innerbox}>
                {loading?"":Clicker.map((item,key)=><ul style={{'margin':'0px'}}><button onClick={()=>handleClick(key)}>{item}</button></ul>)}
            </div>
            <XYPlot height={200} width={250} xType="time" className={styles.innerbox} >
                <HorizontalGridLines style={{ color: 'white' }} />
                <VerticalGridLines />
                <XAxis />
                <YAxis />
                <LineSeries
                    className="first-series"

                    lineStyle={{ stroke: '#7b6060' }}
                    data={chart.map(sto => {
                        return { x: new Date(sto['date_1']).getTime(), y: parseFloat(sto[Clicker[idclicked]]) }
                    }).filter(dat => dat)}
                />
            </XYPlot>
        </div>
    )
}
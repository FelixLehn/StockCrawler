import React, { useState, useEffect } from 'react';
import styles from "./landing-page.module.scss";
import { XYPlot, ChartLabel, VerticalGridLines, HorizontalGridLines, XAxis, YAxis, LineMarkSeries } from 'react-vis';
import axios from "axios";
import '../node_modules/react-vis/dist/style.css';

const LandingPage = props => {
    const [stocks1, setStocks] = useState([]);
    const [stocks2, setStocks2] = useState([]);

    useEffect(() => {
        const stockfetcher = async (n) => {
            const result=await axios.post('http://localhost:5000/api/stocks', { number: n })
                .then(res => res.data)
            return result
        }
        stockfetcher(0)
            .then(res=>setStocks(res))
        stockfetcher(1)
            .then(res=>setStocks2(res))
    }, []);

    return (
        <div>
            <div className={styles.landingheader}>
                <h1>Hello in our fancy Stock Web App!</h1>
            </div>
            <div className={styles.outertab}>
                {stocks1.map(stock => (
                    <div className={styles.innertab}>
                        <div className={styles.box}>
                            <p>{stock.Unternehmen}</p>
                        </div>
                        <div className={styles.box} style={{ fontSize: '12px', width: "250px" }}>
                            <XYPlot height={200} width={250} >
                                <HorizontalGridLines style={{ color: 'white' }} />
                                <VerticalGridLines />
                                <XAxis />
                                <YAxis />
                                <LineMarkSeries
                                    className="linemark-series-example"
                                    style={{
                                        strokeWidth: '3px'
                                    }}
                                    lineStyle={{ stroke: '#7b6060' }}
                                    markStyle={{ stroke: '#7b6060' }}
                                    data={Object.keys(stock).map(sto => {
                                        if (sto !== 'Potential_Analyse' && sto !== 'Stats' && sto !== 'Unternehmen') {
                                            if (stock[sto] && stock[sto] !== '-') {
                                                return { x: parseInt(sto.split('e')[0]), y: parseFloat(stock[sto].split('%')[0].replace('.', '').replace(',', '.')) }
                                            }
                                        }
                                    }).filter(dat => dat)}
                                    color='#7b6060'
                                />
                            </XYPlot>
                        </div>
                        <div className={styles.box}>
                            <p>{stock.Potential_Analyse + '% Potential'}</p>
                        </div>
                    </div>
                ))}
            </div>
            <div className={styles.outertab}>
                {stocks2.map(stock => (
                    <div className={styles.innertab}>
                        <div className={styles.box}>
                            <p>{stock.Unternehmen}</p>
                        </div>
                        <div className={styles.box} style={{ fontSize: '12px', width: "250px" }}>
                            <XYPlot height={200} width={250} >
                                <HorizontalGridLines style={{ color: 'white' }} />
                                <VerticalGridLines />
                                <XAxis />
                                <YAxis />
                                <LineMarkSeries
                                    className="linemark-series-example"
                                    style={{
                                        strokeWidth: '3px'
                                    }}
                                    lineStyle={{ stroke: '#7b6060' }}
                                    markStyle={{ stroke: '#7b6060' }}
                                    data={Object.keys(stock).map(sto => {
                                        if (sto !== 'Potential_Analyse' && sto !== 'Stats' && sto !== 'Unternehmen') {
                                            if (stock[sto] && stock[sto] !== '-') {
                                                return { x: parseInt(sto.split('e')[0]), y: parseFloat(stock[sto].split('%')[0].replace('.', '').replace(',', '.')) }
                                            }
                                        }
                                    }).filter(dat => dat)}
                                    color='#7b6060'
                                />
                            </XYPlot>
                        </div>
                        <div className={styles.box}>
                            <p>{stock.Potential_Analyse + '% Potential'}</p>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    )
}
export default LandingPage;
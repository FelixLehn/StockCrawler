import React, { useState, useEffect } from 'react';
import styles from "./landing-page.module.scss";
import { XYPlot, ChartLabel, VerticalGridLines, HorizontalGridLines, XAxis, YAxis, LineMarkSeries } from 'react-vis';
const LandingPage = props => {
    const [stocks, setStocks] = useState([]);

    useEffect(() => {
        const stockfetcher = async () => {
            const result = await fetch('/stocks')
                .then(res => res.json())
            console.log(result)
            setStocks(result)
        }
        stockfetcher()
    }, []);

    return (
        <div>
            <div className={styles.landingheader}>
                <h1>Hello in our fancy Stock Web App!</h1>
            </div>
            <div className={styles.outertab}>
                {stocks.map(stock => (
                    <div className={styles.innertab}>
                        <div className={styles.box}>
                            <p>{stock.Unternehmen}</p>
                        </div>
                        <div className={styles.box} style={{fontSize:'12px'}}>
                            <XYPlot height={200} width={250} >
                                <HorizontalGridLines style={{color:'white'}}/>
                                <VerticalGridLines />
                                <XAxis />
                                <YAxis />
                                <LineMarkSeries
                                    className="linemark-series-example"
                                    style={{
                                        strokeWidth: '3px'
                                    }}
                                    lineStyle={{ stroke: 'red' }}
                                    markStyle={{ stroke: 'blue' }}
                                    data={Object.keys(stock).map(sto => {
                                        if (sto !== 'Potential_Analyse' && sto !== 'Stats' && sto !== 'Unternehmen') {
                                            if (stock[sto] && stock[sto] !== '-') {
                                                return { x: parseInt(sto.split('e')[0]), y: parseFloat(stock[sto].split('%')[0].replace(',', '.')) }
                                            }
                                        }
                                    }).filter(dat => dat)}
                                    color='red'
                                />
                            </XYPlot>
                        </div>
                        <div className={styles.box}>
                            <p>{stock.Potential_Analyse+'% Potential'}</p>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    )
}
export default LandingPage;
import React, { Component, useEffect, useState } from 'react';
import { FaGithubAlt, FaPlus, FaSpinner } from 'react-icons/fa';
import { Slider, RangeSlider } from 'rsuite';
import { Row, Col } from 'react-bootstrap';
import api from '../../services/api';
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';
import Container from '../../components/Container';
import 'rsuite/dist/rsuite.min.css';

const Main = (props) => {
  const [prices, setPrices] = useState([]);
  const [options, setOptions] = useState({ title: {
    text: 'Carregando as cotações...',
    },
    credits: {
      enabled: false
    },
  });



  useEffect(() => {
    (async () => {
      await api.get("/prices/").then(resp => {
        let prices = []

        resp.data.forEach(price => {
          let datePrice = {}
          datePrice.date = price.date
          datePrice.brl = price.rates.BRL
          datePrice.eur = price.rates.EUR
          datePrice.jpy = price.rates.JPY

          prices.push(datePrice)
        })
        
        setPrices(prices)
        
      const options = {
          chart: {
            type: 'spline'
          },
          xAxis: {
            type: 'datetime',
            categories: prices.map(p => p.date).reverse()
          },
          yAxis: {
            title:{
              text: "USD"
            }
          },
          title: {
            text: 'Cotações dos últimos 5 dias em Dólar(USD)'
          },
          series: [
            {
              name: 'BRL',
              data: prices.map(p => p.brl).reverse()
            },
            {
              name: 'EUR',
              data: prices.map(p => p.eur).reverse()
            },
            {
              name: 'JPY',
              data: prices.map(p => p.jpy).reverse()
            },
          ]
        };

        setOptions(options);
      })
    })();
  }, []);



  const handleChange = async(e) => {
    let newPrice = {}
    if (Date.parse(prices[0].date) > Date.parse(prices[4].date)) {
      newPrice = prices.reverse().slice(e[0]-1, e[1]);
    } else {
      newPrice = prices.slice(e[0]-1, e[1]);
    }

    const options = {
      xAxis: {
        type: 'datetime',
        categories: newPrice.map(p => p.date)
      },
      series: [
        {
          name: 'BRL',
          data: newPrice.map(p => p.brl)
        },
        {
          name: 'EUR',
          data: newPrice.map(p => p.eur)
        },
        {
          name: 'JPY',
          data: newPrice.map(p => p.jpy)
        },
      ]
    };  
    setOptions(options);
    }
    return (
      <>
      <Container>
        <HighchartsReact highcharts={Highcharts} allowChartUpdate={true}
        options={options} />
        <Col md={2} style={{ margin: 'auto', padding: '10px', width: '75%', justifyContent: 'center', textAlign: 'center'}}>
          <div style={{ height: '400px' }}>
            <RangeSlider defaultValue={5}
                          step={1}
                          graduated
                          progress
                          min={1}
                          max={5} 
                          onChange={(e) => handleChange(e)}
                          renderMark={mark => {
                            return <span>{mark}º dia</span>;
                          }} />
          </div>
        </Col>
      </Container>
      </>
    );
  
}

export default Main;

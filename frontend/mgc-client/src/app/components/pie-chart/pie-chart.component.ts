import { Component, HostListener, Input, OnInit } from '@angular/core';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

@Component({
  selector: 'app-pie-chart',
  templateUrl: './pie-chart.component.html',
  styleUrls: ['./pie-chart.component.scss'],
})
export class PieChartComponent implements OnInit {
  @Input() data: { labels: string[]; values: number[] } | null = null;

  chart: Chart | null = null;

  constructor() {}

  ngOnInit(): void {
    if (this.data) {
      this.initializeChart();
    }
  }

  initializeChart(): void {
    const canvas = document.getElementById('pieChart') as HTMLCanvasElement;
    const ctx = canvas.getContext('2d');

    if (ctx && this.data) {
      this.chart = new Chart(ctx, {
        type: 'pie',
        data: {
          labels: this.data.labels,
          datasets: [
            {
              data: this.data.values,
              backgroundColor: [
                '#FF6384',
                '#36A2EB',
                '#FFCE56',
                '#4BC0C0',
                '#9966FF',
                '#0074D9',
                '#FF851B',
                '#A2786F',
                '#3C7633',
                '#2ECC40',
              ],
            },
          ],
        },
        options: {
          plugins: {
            legend: {
              display: true,
              position: 'top',
              labels: {
                font: {
                  size: 12,
                },
                padding: 12,
              },
            },
            tooltip: {
              displayColors: false,
              padding: 8,
              callbacks: {
                label: (context) => {
                  return (context.parsed * 100).toFixed(2) + '%';
                },
              },
            },
          },
        },
      });
    }
  }
  @HostListener('window:resize', ['$event'])
  onResize() {
    if (this.chart) {
      this.chart.resize(); // Wymuszenie odświeżenia rozmiaru
    }
  }
}

import { AfterViewInit, Component, ViewChild, OnInit } from '@angular/core';

import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';

import { AppointmentsService } from 'src/app/services/appointments-service/appointments.service';

export interface AppointmentData {
  appointment_id: string;
  customer_id: string;
  customer_name: string;
  date: string;
  slot: string;
  tests: string;
  doctor_id: string;
  doctor: string;
  nurse_id: string;
  nurse: string;
  lab_technician_id: string;
  lab_technician: string;
  sample_collector_id: string;
  sample_collector: string;
  status: string;
}


@Component({
  selector: 'app-display-appointments',
  templateUrl: './display-appointments.component.html',
  styleUrls: ['./display-appointments.component.css'],
})

export class DisplayAppointmentsComponent implements AfterViewInit, OnInit {

  appointments: any;
  dataSource : MatTableDataSource<AppointmentData>;

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  constructor(private appointments_service: AppointmentsService) {
    this.dataSource = new MatTableDataSource(this.appointments);
  }

  displayedColumns: string[] = [
    'appointment id',
    'customer id',
    'customer name',
    'date',
    'slot',
    // 'tests',
    'doctor id',
    'doctor',
    'nurse id',
    'nurse',
    'lab technician id',
    'lab technician',
    'sample collector id',
    'sample collector',
    'status',
  ];

  ngOnInit(): void {
    this.appointments_service.getAppointments().subscribe({
      next: (data:any) => {
        console.log(data);
        this.appointments = data.appointments;
        console.log("Before",this.appointments)
        this.appointments = JSON.parse(this.appointments);
        console.log("After",this.appointments)
      },
      error: (err) => {
        alert(err);
      },
    });
  }

  ngAfterViewInit() {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();

    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage();
    }
  }
}

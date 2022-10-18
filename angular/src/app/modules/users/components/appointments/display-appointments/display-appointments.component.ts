import { AfterViewInit, Component, ViewChild, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';

import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { MatAccordion } from '@angular/material/expansion';

import { AppointmentsService } from 'src/app/services/appointments-service/appointments.service';
import { CloseDialogComponent } from '../../close-dialog/close-dialog.component';
import { Router } from '@angular/router';
import { SubjectServiceService } from 'src/app/services/subject-service/subject-service.service';

export interface AppointmentData {
  appointment_id: string;
  customer_id: string;
  customer_name: string;
  // date: string;
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

export interface AppointmentsStatusData{
  appointment_id: string;
  customer_id: string;
  customer_name: string;
  slot: string;
  tests: string;
}

@Component({
  selector: 'app-display-appointments',
  templateUrl: './display-appointments.component.html',
  styleUrls: ['./display-appointments.component.css'],
})
export class DisplayAppointmentsComponent implements AfterViewInit, OnInit {
  appointments: any;
  pendingAppointments: any=[];
  approvedAppointments: any=[];
  rejectedAppointments: any=[];
  completedAppointments: any=[];
  tests: any;
  dataSource: MatTableDataSource<AppointmentData>;
  pendingAppointmentsDataSource!: MatTableDataSource<AppointmentsStatusData>;
  approvedAppointmentsDataSource!: MatTableDataSource<AppointmentsStatusData>;
  rejectedAppointmentsDataSource!: MatTableDataSource<AppointmentsStatusData>;
  completedAppointmentsDataSource!: MatTableDataSource<AppointmentsStatusData>;
  login_details: any;
  user_id: any;
  user_type!: string;
  user_username!: string;
  isAdmin: boolean = false;
  role!: string;
  isDoctor: boolean = false;

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;
  @ViewChild(MatAccordion) accordion!: MatAccordion;

  constructor(private appointments_service: AppointmentsService , public dialog: MatDialog , private router :Router, private subjectService : SubjectServiceService) {
    this.dataSource = new MatTableDataSource(this.appointments);
  }

  displayedColumns!: string[];

  getAppointments() {
    this.login_details = window.localStorage.getItem('login_details');
    this.login_details = JSON.parse(this.login_details);
    // this.subjectService.userTypeIdSubject.subscribe(id =>{
    //     this.user_id= id
    // })
    // this.subjectService.userTypeSubject.subscribe(user_type =>{
    //   this.user_type= user_type
    // })
    console.log(this.login_details)
    this.user_id = this.login_details.user_type_id;
    this.user_type = this.login_details.user_type;
    this.user_username = this.login_details.username;
    // console.log(this.user_id,this.user_type)
    this.appointments_service.getAppointments(this.user_username).subscribe({
      next: (data: any) => {
        console.log(this.user_id)
        this.appointments = data.appointments;
        this.tests = data.related_tests;
        if (this.tests != "") {
          this.tests = JSON.parse(this.tests);
        }
        this.appointments = JSON.parse(this.appointments);
        this.dataSource.data = this.appointments;
        this.role=data.role
        console.log(this.appointments, this.tests,this.role)
        this.setAppointmentsAccordingToUser();
      },
      error: (err) => {
        console.log(err);
      },
    });
  }

  setAppointmentsAccordingToUser() {
    if (this.role === "Admin") {
      this.displayedColumns = [
      // this.displayedColumnsForAdmin = [
        'appointment id',
        'customer id',
        'customer name',
        // 'date',
        'slot',
        'doctor id',
        'doctor',
        'nurse id',
        'nurse',
        'lab technician id',
        'lab technician',
        'sample collector id',
        'sample collector',
        'status',
        'tests',
        'delete',
        'update',
      ];
      // this.isAdmin = true;
      // this.displayedColumns = this.displayedColumnsForAdmin;
    }
    else if (this.role === "Doctor") {
      this.appointments.map(
        (appointment: any) => {
          if (appointment.status === "pending") {
            this.pendingAppointments.push(appointment)
          }
          else if (appointment.status === "approved") {
            this.approvedAppointments.push(appointment)
          }
          else if (appointment.status === "rejected") {
            this.rejectedAppointments.push(appointment)
          }
          else if (appointment.status === "completed") {
            this.completedAppointments.push(appointment)
          }
          this.pendingAppointmentsDataSource.data = this.pendingAppointments;
          this.approvedAppointmentsDataSource.data = this.approvedAppointments;
          this.rejectedAppointmentsDataSource.data = this.rejectedAppointments;
          this.completedAppointmentsDataSource.data = this.completedAppointments;
        }
      )
      this.displayedColumns = [
      // this.DisplayedColumnsForStaff = [
        'appointment id',
        'customer id',
        'customer name',
        // 'date',
        'slot',
        'tests',
        'status',
        'update status'
      ];
      // this.displayedColumns = this.DisplayedColumnsForStaff;
    }
  }

  ngOnInit(): void {
    this.getAppointments()
  }



  ngAfterViewInit() {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }

  getDisplayedColumns():string[] {
    return this.columnDefinitions.filter(cd=>!cd.hide).map(cd=>cd.def);
  }

  approveAppointment(id: any) {
    this.appointments_service.approveAppointment(id)
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();

    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage();
    }
  }
  openDialog(id: any) {
    let dialogRef = this.dialog.open(CloseDialogComponent)

    dialogRef.afterClosed().subscribe(result => {
      console.log(result);
      if (result == 'true') {
        this.appointments_service.deleteAppointment(id).subscribe({
          next: (res) => {
            console.log(res);
            this.getAppointments()
          }
        })
      }
    })
  }
  submitDelete(appId: any) {
    console.log("delete");
    this.appointments_service.deleteAppointment(appId).subscribe({
      next: (res) => {
        console.log(res);
        this.getAppointments()
      }
    })
  }

  updateAppointment(id : any){
    this.router.navigate(['admin/edit-appointment' , id])
  }
}

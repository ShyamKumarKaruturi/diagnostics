import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { HttpServiceService } from 'src/app/modules/users/http-service.service';
import { AppointmentsService } from 'src/app/services/appointments-service/appointments.service';
import { CustomerServiceService } from 'src/app/modules/customer/customer-service.service';
import { HttpService } from 'src/app/services/http-service/http.service';

@Component({
  selector: 'app-book-appointment',
  templateUrl: './book-appointment.component.html',
  styleUrls: ['./book-appointment.component.css']
})
export class BookAppointmentComponent implements OnInit {
  formNotValid: boolean = false
  formError?: string = ""
  status_arr: string[] = ['booked', 'completed', 'approved', 'rejected', 'pending']
  slots: string[] = ['10 AM', "1 PM", '4 PM']
  labTechnicians: any;
  sampleCollectors: any;
  nurse: any
  isEmployee: boolean = true;
  users: any;
  tests: any;
  branches: any
  doctors: any;
  nurses: any;
  lab_technicians: any;
  sample_collectors: any;
  user: any = window.localStorage.getItem('user')
  user_data: any = JSON.parse(this.user)
  user_info_data: any = window.localStorage.getItem('user_data')
  user_info: any = JSON.parse(this.user_info_data)


  constructor(private http: CustomerServiceService, private router: Router,
    private appointment_service: AppointmentsService,
    private httpUser: HttpServiceService, private httpService: HttpService) { }

  bookAppointmentForm: FormGroup = new FormGroup({
    user: new FormControl("", Validators.required),
    doctor_id: new FormControl("", Validators.required),
    branch: new FormControl(null, Validators.required),
    nurse_id: new FormControl("", Validators.required),
    lab_technician: new FormControl("", Validators.required),
    sample_collector: new FormControl("", Validators.required),
    status: new FormControl("", Validators.required),
    slot: new FormControl("", Validators.required),
    tests: new FormControl("",Validators.required),
  })

  ngOnInit(): any {

    this.httpService.getDetailsForAppointmentBooking().subscribe({
      next: (data: any) => {
        this.users = data.users;
        this.users = JSON.parse(this.users);
        this.branches = data.branches;
        this.branches = JSON.parse(this.branches);
        this.tests = data.tests;
        this.tests = JSON.parse(this.tests);
        this.doctors = data.doctors;
        this.doctors = JSON.parse(this.doctors);
        this.nurses = data.nurses;
        this.nurses = JSON.parse(this.nurses);
        this.lab_technicians = data.lab_technicians;
        this.lab_technicians = JSON.parse(this.lab_technicians);
        this.sample_collectors = data.sample_collectors;
        this.sample_collectors = JSON.parse(this.sample_collectors);
        console.log(this.users,this.branches,this.tests,this.doctors,this.nurses,this.lab_technicians,this.sample_collectors)
      },
      error: (err) => {
        console.log(err.data);
      },
    })

    console.log(this.user_data['is_employee'], this.user_data, typeof (this.user_data))
    if (this.user_data['is_employee']) {
      this.isEmployee = true;
    }
    else {
      this.isEmployee = false;
      this.bookAppointmentForm.controls['user'].setValue(this.user_data['username']);
    }
    //   console.log(this.bookAppointmentForm.getRawValue(), this.isEmployee);
    //   this.httpUser.getBranches().subscribe(data => {
    //     this.branches = data
    //     console.log(this.branches)})
    //   this.http.getDoctors().subscribe(data => {
    //     this.doctors = data
    //     console.log(this.doctors);
    //     })
      // this.http.getLabTechnician().subscribe(data => {
      //   this.labTechnicians= data
      //   console.log(this.labTechnicians);
      // })
    //   this.http.getNurse().subscribe(data => {
    //     this.nurse = data
    //     console.log(this.nurse);
    //   })
    //   this.http.getSampleCollector().subscribe(data => {
    //     this.sampleCollectors = data
    //     console.log(this.sampleCollectors);
    //   })
    // }

    // 'username': this.bookAppointmentForm.get('username')?.value
  }
  bookAppointment() {
    this.bookAppointmentForm.controls['user'].setValue(this.user_info['customer_id']);
      console.log(this.bookAppointmentForm.value);
      this.appointment_service.setAppointment({ 'form': this.bookAppointmentForm.value, 'username': window.localStorage.getItem('username') }).subscribe(data => {
        console.log(data);

      })
  }
}

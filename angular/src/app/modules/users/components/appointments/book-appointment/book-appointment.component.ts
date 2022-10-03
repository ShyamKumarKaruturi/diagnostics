import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { HttpServiceService } from 'src/app/modules/users/http-service.service';
import { AppointmentsService } from 'src/app/services/appointments-service/appointments.service';
import { CustomerServiceService } from 'src/app/modules/customer/customer-service.service';

@Component({
  selector: 'app-book-appointment',
  templateUrl: './book-appointment.component.html',
  styleUrls: ['./book-appointment.component.css']
})
export class BookAppointmentComponent implements OnInit {
  formNotValid: boolean = false
  formError?: string = ""
  status_arr: string[] = ['booked','completed','approved', 'rejected', 'pending']
  slots : string[] = ['10 AM', "1 PM",'4 PM']
  branches: any
  doctors :any
  labTechnicians :any
  sampleCollectors :any
  nurse: any
  isEmployee: boolean = true;
  user : any = window.localStorage.getItem('user')
  user_data: any = JSON.parse(this.user)



  constructor(private http: CustomerServiceService, private router: Router,
    private appointment_service: AppointmentsService,
    private httpUser : HttpServiceService) { }

  bookAppointmentForm: FormGroup = new FormGroup({
    username: new FormControl("", Validators.required),
    doctor_id: new FormControl("", Validators.required),
    branch: new FormControl(null , Validators.required),
    nurse_id: new FormControl("", Validators.required),
    lab_technician: new FormControl("", Validators.required),
    sample_collector: new FormControl("", Validators.required),
    status: new FormControl("", Validators.required),
    slot: new FormControl("", Validators.required),
  })

  ngOnInit(): any {
    console.log(this.user_data['is_employee'],this.user_data, typeof(this.user_data))
    if (this.user_data['is_employee']) {
      this.isEmployee = true;
    }
    else {
      this.isEmployee = false;
      this.bookAppointmentForm.controls['username'].setValue(this.user_data['username']);
    }
    console.log(this.bookAppointmentForm.getRawValue(), this.isEmployee);
    this.httpUser.getBranches().subscribe(data => {
      this.branches = data
      console.log(this.branches)})
    this.http.getDoctors().subscribe(data => {
      this.doctors = data
      console.log(this.doctors);
      })
    this.http.getLabTechnician().subscribe(data => {
      this.labTechnicians= data
      console.log(this.labTechnicians);
    })
    this.http.getNurse().subscribe(data => {
      this.nurse = data
      console.log(this.nurse);
    })
    this.http.getSampleCollector().subscribe(data => {
      this.sampleCollectors = data
      console.log(this.sampleCollectors);
    })


  }

  // 'username': this.bookAppointmentForm.get('username')?.value

  bookAppointment(){
    console.log(this.bookAppointmentForm.value);
    this.appointment_service.setAppointment({ 'form': this.bookAppointmentForm.value, 'username': window.localStorage.getItem('username') }).subscribe(data=>{
      console.log(data);

    })
  }
}

import { Component, OnInit } from '@angular/core';
import { CustomerService } from 'src/app/services/customer-service/customer.service';
import { SubjectServiceService } from 'src/app/services/subject-service/subject-service.service';
import { CustomerServiceService } from '../../customer-service.service';

@Component({
  selector: 'app-appointments',
  templateUrl: './appointments.component.html',
  styleUrls: ['./appointments.component.css']
})
export class AppointmentsComponent implements OnInit {

  customer_id :string =''
  appointments :any
  tests : any
  constructor(private subjectService: SubjectServiceService , private http: CustomerService)  {
      this.customer_id = localStorage.getItem("customerId") || ""
   }
  ngOnInit(): void {
    this.http.getCustomerAppointments(this.customer_id).subscribe({
      next:(data :any)=>{
        this.appointments = data.appointments
        this.tests = data.related_tests;
        this.tests = JSON.parse(this.tests);
        this.appointments = JSON.parse(this.appointments);
        console.log(data);
         },
      error: (err) => {
        console.log(err);
      },
    })
  }


}

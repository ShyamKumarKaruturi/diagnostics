import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HttpService } from 'src/app/services/http-service/http.service';

export interface Customer{
  customer_id:string,
  user_id : any
}

@Component({
  selector: 'app-display-customer',
  templateUrl: './display-customer.component.html',
  styleUrls: ['./display-customer.component.css']
})
export class DisplayCustomerComponent implements OnInit {
  customer_id : string =''
  customerDetails : any
  UserDetails : any
  appointments: any
  constructor(private actRouter: ActivatedRoute, private http: HttpService) { 
    this.actRouter.params.subscribe(data => {
      this.customer_id = data['cutomer_id']
    })
    this.http.getCustomer(this.customer_id).subscribe({
      next: (data: any) => {
        this.customerDetails = data["customer_details"]
        this.UserDetails = data["user_details"]
        this.appointments = data["appointments"]
      },
      error: (err) => {
        console.log(err.error.detail);
      }
    })
  }
  ngOnInit(): void {
    
    

  }

}

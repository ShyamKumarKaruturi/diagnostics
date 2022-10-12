import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AppointmentsService } from 'src/app/services/appointments-service/appointments.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  user = ""
  constructor(
    private http: HttpClient  ,
    private router: Router,
  ) { }

  ngOnInit(): void {
    this.http.get("http://127.0.0.1:8000/users/user/").subscribe({
      next: (resp: any) => {
        this.user = resp.username
      },
      error: () => {
        this.router.navigate(['users/login'])
      }
    })
  }

}

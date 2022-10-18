import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import {BehaviorSubject} from 'rxjs'
@Injectable({
  providedIn: 'root'
})

export class SubjectServiceService {

  loggedIn : boolean = false
  public usernameSubject = new BehaviorSubject("");
  public isLoggedInSubject =  new BehaviorSubject(false)
  public userTypeSubject = new BehaviorSubject("customer")
  public userTypeIdSubject = new BehaviorSubject("")

  constructor(
    private http: HttpClient,
    private router: Router,
  ) {
    this.http.get("http://127.0.0.1:8000/users/user/").subscribe({
      next: (data: any) => {
        this.usernameSubject.next(data['username'])
        this.isLoggedInSubject.next(true)
        this.userTypeSubject.next(data['user_type'])
        this.userTypeIdSubject.next(data['user_type_id'])
        this.loggedIn = true
      },
      error: () => {
        this.usernameSubject.next("")
        this.isLoggedInSubject.next(false)
        this.userTypeSubject.next("customer")
        this.userTypeIdSubject.next("")
        this.loggedIn = false
      }
    })
   }

  sendLoginDetails(data : any){
    this.usernameSubject.next(data['username'])
    this.isLoggedInSubject.next(true)
    this.userTypeSubject.next(data['user_type'])
    this.userTypeIdSubject.next(data['user_type_id'])
    this.loggedIn = true
    window.localStorage.setItem('login_details', JSON.stringify(data))
  }

  logoutService(){
    this.usernameSubject.next("")
    this.isLoggedInSubject.next(false)
    this.userTypeSubject.next("customer")
    this.userTypeIdSubject.next("")
    this.loggedIn = false
  }
}

import { NonNullAssert } from '@angular/compiler';
import { Component, OnInit } from '@angular/core';
import { SubjectServiceService } from 'src/app/services/subject-service/subject-service.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {
  loggedIn : any
  userType : string=''
  constructor(private subjectService : SubjectServiceService) { }

  ngOnInit(): void {
    this.subjectService.isLoggedInSubject.subscribe(data=>{
      this.loggedIn = data
    })
    this.subjectService.userTypeSubject.subscribe(data=>{
      this.userType = data
    })
  }
}

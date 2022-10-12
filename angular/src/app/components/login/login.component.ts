import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthInterceptor } from 'src/app/interceptors/auth.interceptor';
import { HttpServiceService } from 'src/app/modules/users/http-service.service';
import { SubjectServiceService } from 'src/app/services/subject-service/subject-service.service';
@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent implements OnInit {
  hide: boolean = false;
  formNotValid: boolean = false;
  responseMessage: string = '';
  constructor(private http: HttpServiceService, private router: Router, private subjectService: SubjectServiceService) { }

  loginForm: FormGroup = new FormGroup({
    username: new FormControl('', Validators.required),
    password: new FormControl('', Validators.required),
  });
  handleError(err: any) {
    // alert(err)
  }
  submitLogin() {
    this.http.loginUser(this.loginForm.value).subscribe({
      next: (resp: any) => {
        this.responseMessage = resp.message
        if (resp.message == "success") {
          AuthInterceptor.accessToken = resp.token;
          this.subjectService.sendLoginDetails({
            'user_type': resp.user_type,
            'username': resp.username,
            'user_type_id': resp.user_type_id
          })
          this.router.navigate([""])
        }
      },
      error: (err: any) => {
        console.log(err);
      }
    })
  }

  ngOnInit(): void { }
}

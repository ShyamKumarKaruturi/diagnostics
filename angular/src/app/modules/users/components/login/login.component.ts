import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { HttpServiceService } from '../../http-service.service';
import { Router } from '@angular/router';
@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent implements OnInit {
  hide: boolean = false;
  formNotValid: boolean = false;
  errorMessage: string = '';
  constructor(private http: HttpServiceService, private router: Router) {}

  loginForm: FormGroup = new FormGroup({
    username: new FormControl('', Validators.required),
    password: new FormControl('', Validators.required),
  });
  handleError(err: any) {
    // alert(err)
  }
  submitLogin() {
    if (this.loginForm.valid) {
      this.formNotValid = false

      this.http.loginUser(this.loginForm.value).subscribe({
        next: (resp) => {
          console.log(resp);
          this.errorMessage = resp.msg;
          if (this.errorMessage == 'logged in') {
            this.http.saveData('username', resp.user.username);
            this.http.saveData('user_type', resp.user.user_type);
            // console.log(this.http.getData('username'));
            localStorage.setItem('user', JSON.stringify(resp.user));
            localStorage.setItem('user_data',JSON.stringify(resp.user_data))
            this.router.navigate(['']);
          }
        },
        error: (err) => {
          console.log(err.data);
          this.handleError(err.message);
        },
      });
    } else {
      console.log('fill properly ');
      this.formNotValid = true;
      console.log(this.loginForm.valid);
    }
  }

  ngOnInit(): void {}
}

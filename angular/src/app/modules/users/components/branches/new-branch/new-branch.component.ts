import { Component, OnInit } from '@angular/core';
import { BranchesService } from 'src/app/services/branches-service/branches.service';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-new-branch',
  templateUrl: './new-branch.component.html',
  styleUrls: ['./new-branch.component.css']
})
export class NewBranchComponent implements OnInit {

  constructor(private http: BranchesService, private router: Router) { }
  responseMessage: string = '';
  formNotValid: boolean = false;

  branchForm: FormGroup = new FormGroup({
    branch_id: new FormControl('', Validators.required),
    branch_name: new FormControl('', Validators.required),
    location: new FormControl('', Validators.required),  
  });

  onSubmit(){
    if(this.branchForm.valid){
      this.formNotValid = false
      this.http.addBranch({ 'form': this.branchForm.value }).subscribe({
        next: (resp) => {
          this.responseMessage = resp.message
          if (resp.action_status == "success") {
            this.router.navigate([''])
          }
        },
        error: (err) => {
          console.log(err);
        }
      })
    }
    else{
      this.formNotValid = true
    }
  }
  ngOnInit(): void {
  }
}

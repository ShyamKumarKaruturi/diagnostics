import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BookAppointmentComponent } from './components/appointments/book-appointment/book-appointment.component';
import { DisplayAppointmentsComponent } from './components/appointments/display-appointments/display-appointments.component';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { LoginComponent } from './components/login/login.component';
import { LogoutComponent } from './components/logout/logout.component';
import { RegisterCustomerComponent } from './components/register-customer/register-customer.component';
import { RegisterEmployeeComponent } from './components/register-employee/register-employee.component';

const routes: Routes = [
  {path:"",component:DashboardComponent,children:[
    {path:'register-customer' , component : RegisterCustomerComponent },
    { path: 'register-employee', component: RegisterEmployeeComponent },
    { path: 'login', component: LoginComponent},
    { path: 'logout', component: LogoutComponent },
    { path: 'book-appointment', component: BookAppointmentComponent },
    {path:'display-appointments',component: DisplayAppointmentsComponent},

    {path : '', redirectTo:'register-customer',pathMatch:"full"}
  ]}
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class UsersRoutingModule { }

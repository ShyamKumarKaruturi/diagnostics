import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BookAppointmentComponent } from '../users/components/appointments/book-appointment/book-appointment.component';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { DisplayAppointmentsComponent } from './components/display-appointments/display-appointments.component';

const routes: Routes = [
  {
    path: "", component: DashboardComponent, children: [
      { path: 'display-appointments', component: DisplayAppointmentsComponent },
      { path: '', redirectTo: 'display-appointments', pathMatch: "full" },
      {path:'book-appointment', component: BookAppointmentComponent},
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AdminRoutingModule { }

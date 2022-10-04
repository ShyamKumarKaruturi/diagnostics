import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { AdminRoutingModule } from './admin-routing.module';
import { DisplayAppointmentsComponent } from './components/display-appointments/display-appointments.component';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import {  MatIconModule } from '@angular/material/icon';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatTableModule } from '@angular/material/table';

@NgModule({
  declarations: [
    DashboardComponent,
    DisplayAppointmentsComponent,
  ],
  imports: [
    CommonModule,
    AdminRoutingModule,
    MatIconModule,
    MatToolbarModule,
    MatTableModule
  ]
})
export class AdminModule { }

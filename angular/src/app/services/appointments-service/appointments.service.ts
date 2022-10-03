import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

const baseUrl = 'http://127.0.0.1:8000/';

@Injectable({
  providedIn: 'root',
})
export class AppointmentsService {
  constructor(private http: HttpClient) {}

  // Appointments Services.

  getAppointments(): Observable<Object> {
    return this.http.get<any>(`${baseUrl}${'appointments/appointment/'}`);
  }

  getAppointment(id: any): Observable<Object> {
    return this.http.get<any>(`${baseUrl}${'appointments/appointment/'}`, id);
  }

  setAppointment(data: any) {
    return this.http.post<any>(`${baseUrl}${'appointments/book-appointment/'}`, data);
  }

  updateAppointment(data: any) {
    return this.http.put<any>(`${baseUrl}${'appointments/appointment/'}`, data);
  }

  deleteAppointment(data: any) {
    return this.http.delete<any>(
      `${baseUrl}${'appointments/appointment/'}`,
      data
    );
  }
}

import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

const baseUrl = 'http://127.0.0.1:8000/';

@Injectable({
  providedIn: 'root',
})
export class AppointmentsService {
  constructor(private http: HttpClient) { }

  // Appointments Services.

  getAppointments(username: any): Observable<Object> {
    return this.http.get<any>(`${baseUrl}${'appointments/book-appointment/'}`, { params: { 'username': username } });
  }
  setAppointment(data: any) {
    return this.http.post<any>(`${baseUrl}${'appointments/book-appointment/'}`, data);
  }

  getAppointment(id: any): Observable<Object> {
    return this.http.get<any>(`${baseUrl}appointments/appointment/${id}/`);
  }

  updateAppointment(id: any, data: any) {
    return this.http.put<any>(`${baseUrl}appointments/appointment/${id}/`, data);
  }

  deleteAppointment(id: any) {
    return this.http.delete<any>(
      `${baseUrl}appointments/appointment/${id}/`
    );
  }

  changeAppointmentStatus(id: any, status: string) {
    return this.http.post<any>(`${baseUrl}${'appointments/update-appointment-status/'}`, { params: { 'id': id, 'status': status } });
  }

}

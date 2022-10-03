import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

const baseUrl = 'http://127.0.0.1:8000/';

@Injectable({
  providedIn: 'root',
})
export class LabsService {
  constructor(private http: HttpClient) {}

  // Lab Services
  getLabs(): Observable<Object> {
    return this.http.get<any>(`${baseUrl}${'appointments/lab/'}`);
  }

  getLab(id: any): Observable<Object> {
    return this.http.get<any>(`${baseUrl}${'appointments/lab/'}`, id);
  }

  setLab(data: any) {
    return this.http.put<any>(`${baseUrl}${'appointments/lab/'}`, data);
  }

  updateLab(data: any) {
    return this.http.put<any>(`${baseUrl}${'appointments/lab/'}`, data);
  }

  deleteLab(data: any) {
    return this.http.delete<any>(`${baseUrl}${'appointments/lab/'}`, data);
  }
}

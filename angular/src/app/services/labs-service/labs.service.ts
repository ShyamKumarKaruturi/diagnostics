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
  createLab(data:any){
    return this.http.post<any>(`${baseUrl}${'appointments/labs/'}`, data);
  }
  getLabs(): Observable<Object> {
    return this.http.get<any>(`${baseUrl}${'appointments/labs/'}`);
  }

  getLab(id: any): Observable<Object> {
    return this.http.get<any>(`${baseUrl}${'appointments/labs/'}`, id);
  }

  setLab(data: any) {
    return this.http.put<any>(`${baseUrl}${'appointments/labs/'}`, data);
  }

  updateLab(data: any) {
    return this.http.put<any>(`${baseUrl}${'appointments/labs/'}`, data);
  }

  deleteLab(data: any) {
    return this.http.delete<any>(`${baseUrl}${'appointments/labs/'}`, data);
  }
}

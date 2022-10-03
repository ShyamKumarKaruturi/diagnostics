import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

const baseUrl = 'http://127.0.0.1:8000/';

@Injectable({
  providedIn: 'root',
})
export class BillsService {
  constructor(private http: HttpClient) {}

  // Bill Services

  getBills(): Observable<Object> {
    return this.http.get<any>(`${baseUrl}${'appointments/bill/'}`);
  }

  getBill(id: any): Observable<Object> {
    return this.http.get<any>(`${baseUrl}${'appointments/bill/'}`, id);
  }

  setBill(data: any) {
    return this.http.put<any>(`${baseUrl}${'appointments/bill/'}`, data);
  }

  updateBill(data: any) {
    return this.http.put<any>(`${baseUrl}${'appointments/bill/'}`, data);
  }

  deleteBill(data: any) {
    return this.http.delete<any>(`${baseUrl}${'appointments/bill/'}`, data);
  }
}

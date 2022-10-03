import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

const baseUrl = 'http://127.0.0.1:8000/';

@Injectable({
  providedIn: 'root',
})
export class TestsService {
  constructor(private http: HttpClient) {}

  // Test Services

  getTests(): Observable<Object> {
    return this.http.get<any>(`${baseUrl}${'appointments/test/'}`);
  }

  getTest(id: any): Observable<Object> {
    return this.http.get<any>(`${baseUrl}${'appointments/test/'}`, id);
  }

  setTest(data: any) {
    return this.http.put<any>(`${baseUrl}${'appointments/test/'}`, data);
  }

  updateTest(data: any) {
    return this.http.put<any>(`${baseUrl}${'appointments/test/'}`, data);
  }

  deleteTest(data: any) {
    return this.http.delete<any>(`${baseUrl}${'appointments/test/'}`, data);
  }
}

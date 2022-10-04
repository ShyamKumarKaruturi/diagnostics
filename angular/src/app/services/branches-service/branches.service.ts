import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

const baseUrl = 'http://127.0.0.1:8000/';

@Injectable({
  providedIn: 'root',
})
export class BranchesService {
  constructor(private http: HttpClient) { }

  // Branch Services
  addBranch(data: any) {
    return this.http.post<any>(`${baseUrl}${'appointments/branches/'}`, data);
  }

  getBranches(): Observable<Object> {
    return this.http.get<any>(`${baseUrl}${'appointments/branches/'}`);
  }

  getBranch(id: any): Observable<Object> {
    return this.http.get<any>(`${baseUrl}${'appointments/branches'}`, id);
  }

  setBranch(data: any) {
    return this.http.put<any>(`${baseUrl}${'appointments/branches'}`, data);
  }

  updateBranch(data: any) {
    return this.http.put<any>(`${baseUrl}${'appointments/branches'}`, data);
  }

  deleteBranch(data: any) {
    return this.http.delete<any>(`${baseUrl}${'appointments/branches'}`, data);
  }
}

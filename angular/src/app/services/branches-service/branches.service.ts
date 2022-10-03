import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

const baseUrl = 'http://127.0.0.1:8000/';

@Injectable({
  providedIn: 'root',
})
export class BranchesService {
  constructor(private http: HttpClient) {}

  // Branch Services

  getBranches(): Observable<Object> {
    return this.http.get<any>(`${baseUrl}${'appointments/branch/'}`);
  }

  getBranch(id: any): Observable<Object> {
    return this.http.get<any>(`${baseUrl}${'appointments/branch/'}`, id);
  }

  setBranch(data: any) {
    return this.http.put<any>(`${baseUrl}${'appointments/branch/'}`, data);
  }

  updateBranch(data: any) {
    return this.http.put<any>(`${baseUrl}${'appointments/branch/'}`, data);
  }

  deleteBranch(data: any) {
    return this.http.delete<any>(`${baseUrl}${'appointments/branch/'}`, data);
  }
}

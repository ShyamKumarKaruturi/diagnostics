import { AfterViewInit, Component, ViewChild, OnInit } from '@angular/core';

import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { MatAccordion } from '@angular/material/expansion';

import { BillsService } from 'src/app/services/bills-service/bills.service';

export interface BillData{
  bill_id: string;
  appointment_id: string;
  customer_name: string;
  consultation_fee: string;
  test_fee: string;
  tax: string;
  total: string;
}

@Component({
  selector: 'app-display-bills',
  templateUrl: './display-bills.component.html',
  styleUrls: ['./display-bills.component.css']
})
export class DisplayBillsComponent implements AfterViewInit,OnInit {

  bills: any;
  dataSource: MatTableDataSource<BillData>;

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;
  @ViewChild(MatAccordion) accordion!: MatAccordion;

  constructor(private bills_service: BillsService) {
    this.dataSource = new MatTableDataSource(this.bills);
  }

  displayedColumns: string[] = [
    'bill id',
    'appointment id',
    'customer name',
    'consultation fee',
    'test fee',
    'tax',
    'total',
    'update',
    'delete',
  ];
  ngOnInit(): void {
    this.bills_service.getBills().subscribe({
      next: (data: any) => {
        console.log(data);
        this.bills = data.bills;
        this.bills = JSON.parse(this.bills);
        this.dataSource.data = this.bills;
        console.log(this.dataSource);
      },
      error: (err) => {
        console.log(err);
      },
    });
  }

  ngAfterViewInit() {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }
  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();

    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage();
    }
  }
}

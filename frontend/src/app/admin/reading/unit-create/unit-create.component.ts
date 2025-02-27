import {Component, EventEmitter, OnInit, Output} from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-unit-create',
  templateUrl: './unit-create.component.html',
  styleUrls: ['./unit-create.component.scss']
})
export class UnitCreateComponent {

  constructor(private http: HttpClient) {}

  newUnitName: string = "";

  createNewUnit(): void {
    if (!this.newUnitName.trim()) return;
    const payload = { title: this.newUnitName };
    this.http.post<string>('http://localhost:8000/readings/units', payload).subscribe(
      (message) => {
        this.newUnitName = '';
        // this.fetchUnits();
        alert(message); // Gelen mesajı bir uyarı olarak göster
      },
      (error) =>  alert(error.error.detail)
    );
  }

  @Output()
  cancelCreate: EventEmitter<void> = new EventEmitter<void>();

  cancelCreatNewUnit() {
    this.cancelCreate.emit()
  }

}

import {Component, EventEmitter, Input, Output} from '@angular/core';
import {HttpClient} from "@angular/common/http";

interface Unit {
  id: number;
  name: string;
}

interface CreateText {
  "unit_id": number,
  "title": string,
  "context": string
}

interface CreatedText {
  "id": number,
  "unit_name": string,
  "title": string
}

@Component({
  selector: 'app-text-create',
  templateUrl: './text-create.component.html',
  styleUrls: ['./text-create.component.scss']
})
export class TextCreateComponent {

  constructor(private http: HttpClient) {}
  createdText: CreatedText | null = null;
  createText: CreateText = {
    unit_id: 0,
    title: "",
    context: ""
  }

  @Input() unit!: Unit;

  ngOnInit() {
    console.log('Unit:', this.unit);
  }

  @Output() continueCreate: EventEmitter<CreatedText> = new EventEmitter<CreatedText>();
  @Output() cancelCreate: EventEmitter<void> = new EventEmitter<void>();

  createNewText(): void {
    this.createText.unit_id = this.unit.id
    this.http.post<CreatedText>('http://localhost:8000/readings/texts', this.createText).subscribe(
      (created_text) => {
        // this.createdText = created_text
        this.continueCreate.emit(created_text);

      },
      (error) => {
        alert(error.error);
        console.log(error);
      }
    );
  }

  cancelCreateNewText() {
    this.cancelCreate.emit();
  }
}

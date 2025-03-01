import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TextCreateComponent } from './text-create.component';

describe('TextCreateComponent', () => {
  let component: TextCreateComponent;
  let fixture: ComponentFixture<TextCreateComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [TextCreateComponent]
    });
    fixture = TestBed.createComponent(TextCreateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

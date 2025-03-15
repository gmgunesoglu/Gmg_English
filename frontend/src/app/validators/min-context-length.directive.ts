import { Directive, Input } from '@angular/core';
import { NG_VALIDATORS, Validator, AbstractControl, ValidationErrors } from '@angular/forms';

@Directive({
  selector: '[appMinTextLength]',
  providers: [
    {
      provide: NG_VALIDATORS,
      useExisting: MinContextLengthDirective,
      multi: true
    }
  ]
})
export class MinContextLengthDirective implements Validator {

  @Input() appMinTextLength!: string; // HTML'den gelen string değer

  validate(control: AbstractControl): ValidationErrors | null {
    const minLength = Number(this.appMinTextLength); // String'i Number'a çeviriyoruz
    const value = control.value?.trim();
    if (value.length < minLength) {
      return { minTextLength: { requiredLength: minLength, actualLength: value.length } };
    }
    return null;
  }
}

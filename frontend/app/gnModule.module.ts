import { NgModule } from "@angular/core";
import { CommonModule } from '@angular/common';
import { GN2CommonModule } from "@geonature_common/GN2Common.module";
import { Routes, RouterModule } from "@angular/router";
import { IndividualsComponent } from "./individuals-component/individuals.component";


// my module routing
const routes: Routes = [
{path: "individuals", component: IndividualsComponent}];

@NgModule({
  declarations: [ IndividualsComponent],
  imports: [GN2CommonModule, RouterModule.forChild(routes), CommonModule],
  providers: [],
  bootstrap: []
})
export class GeonatureModule {}

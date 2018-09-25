import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { AppConfig } from "@geonature_config/app.config";

@Injectable()
export class IndividualsService {
  constructor(private _api: HttpClient) {}

  getAllIndividuals() {
    console.log('get all individuals.')
    return this._api.get<any>(`${AppConfig.API_ENDPOINT}/individuals`);
  }

  getOneIndividual(id) {
    return this._api.get<any>(`${AppConfig.API_ENDPOINT}/individuals/${id}`);
  }

  deleteIndividual(id) {
    return this._api.delete(`${AppConfig.API_ENDPOINT}/individuals/${id}`);
  }

  postIndividuals(form) {
    return this._api.post(`${AppConfig.API_ENDPOINT}/individuals`, form);
  }

}
